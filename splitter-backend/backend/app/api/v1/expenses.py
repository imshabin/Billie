# backend/app/api/v1/expenses.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ... import models, schemas
from ...dependencies import get_db
from ...auth.security import get_current_user
from ...crud.crudGroup import get_group_by_id
from ...crud.crudExpense import create_expense


router = APIRouter()

@router.post("/groups/{group_id}/expenses", response_model=schemas.Expense, status_code=status.HTTP_201_CREATED)
async def create_expense_for_group(
    group_id: int,
    expense: schemas.ExpenseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Add a new expense to a group.
    - The current user must be a member of the group.
    - All users in the split must also be members of the group.
    """
    group = await get_group_by_id(db=db, group_id=group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

    group_member_ids = {member.id for member in group.members}
    if current_user.id not in group_member_ids:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a member of this group")

    # Validate that all users to be split with are actually in the group
    for user_id in expense.split_between:
        if user_id not in group_member_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with ID {user_id} is not a member of this group."
            )

    new_expense = await create_expense(
        db=db, expense=expense, group_id=group_id, paid_by_id=current_user.id
    )
    return new_expense