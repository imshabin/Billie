# backend/app/crud/expense.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from decimal import Decimal, ROUND_DOWN
from typing import Set

from .. import schemas
from ..models.expense import  Expense, ExpenseSplit
from ..models.group import Group


class ExpenseValidationError(Exception):
    """Custom exception for expense validation errors."""
    pass


async def create_expense(
    db: AsyncSession,
    expense: schemas.ExpenseCreate,
    group_id: int,
    paid_by_id: int
) -> Expense:
    """
    Creates a new expense and its associated equal splits in the database.
    
    Args:
        db: Async database session
        expense: Expense creation schema containing description, amount, and split_between
        group_id: ID of the group this expense belongs to
        paid_by_id: ID of the user who paid for the expense
    
    Returns:
        models.Expense: The created expense with loaded relationships
    
    Raises:
        ExpenseValidationError: If validation fails
        ValueError: If amount is invalid or split_between is empty
    
    Note:
        The function distributes any rounding remainder to the last person
        in the split to ensure total splits equal the original amount.
    """
    try:
        # ========== VALIDATION ==========
        
        # Validate amount
        if expense.amount <= 0:
            raise ValueError("Expense amount must be greater than zero")
        
        # Validate split_between list
        if not expense.split_between:
            raise ValueError("split_between cannot be empty")
        
        # Check for duplicate user IDs
        unique_users: Set[int] = set(expense.split_between)
        if len(unique_users) != len(expense.split_between):
            raise ValueError("split_between contains duplicate user IDs")
        
        # Verify paid_by_id is in the group
        # paid_by_check = await db.execute(
        #     select(Group.members)
        #     .where(
        #         Group.members.id == group_id,
        #         Group.members.id == paid_by_id
        #     )
        # )
        # if not paid_by_check.scalar_one_or_none():
        #     raise ExpenseValidationError(
        #         f"User {paid_by_id} is not a member of group {group_id}"
        #     )
        
        # Verify all users in split_between are in the group
        # members_check = await db.execute(
        #     select(Group.members.id)
        #     .where(
        #         Group.members.id == group_id,
        #         Group.members.user_id.in_(expense.split_between)
        #     )
        # )
        # valid_member_ids = {row[0] for row in members_check.all()}
        
        # invalid_users = unique_users - valid_member_ids
        # if invalid_users:
        #     raise ExpenseValidationError(
        #         f"Users {invalid_users} are not members of group {group_id}"
        #     )
        
        # ========== CALCULATION ==========
        
        # Calculate split amount with proper rounding
        num_members = len(expense.split_between)
        base_split = (expense.amount / Decimal(num_members)).quantize(
            Decimal("0.01"), rounding=ROUND_DOWN
        )
        
        # Calculate remainder to assign to last person
        total_base_splits = base_split * Decimal(num_members)
        remainder = expense.amount - total_base_splits
        
        # ========== DATABASE OPERATIONS ==========
        
        # Create the main Expense object
        db_expense = Expense(
            description=expense.description,
            amount=expense.amount,
            group_id=group_id,
            paid_by_id=paid_by_id,
        )
        db.add(db_expense)
        
        # Flush to get the expense ID
        await db.flush()
        
        # Create ExpenseSplit objects in bulk
        splits = []
        for idx, user_id in enumerate(expense.split_between):
            # Add remainder to the last person's split
            amount_owed = base_split
            if idx == len(expense.split_between) - 1:
                amount_owed += remainder
            
            splits.append(
                ExpenseSplit(
                    expense_id=db_expense.id,
                    owed_by_id=user_id,
                    amount_owed=amount_owed,
                )
            )
        
        # Bulk insert all splits
        db.add_all(splits)
        
        # Commit the transaction
        await db.commit()
        
        # Reload with relationships for response
        result = await db.execute(
            select(Expense)
            .options(
                selectinload(Expense.paid_by),
                selectinload(Expense.splits).selectinload(
                    ExpenseSplit.owed_by
                )
            )
            .where(Expense.id == db_expense.id)
        )
        
        return result.scalars().one()
    
    except (ValueError, ExpenseValidationError) as e:
        # Rollback on validation errors
        await db.rollback()
        raise
    
    except Exception as e:
        # Rollback on any other error
        await db.rollback()
        raise Exception(f"Failed to create expense: {str(e)}") from e