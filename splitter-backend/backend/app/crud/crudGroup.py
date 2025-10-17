# backend/app/crud.py (or wherever your crudGroup is defined)
from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from backend.app.models.group import Group
from backend.app.schemas import GroupCreate

from sqlalchemy.orm import Session
from backend.app.models.user import User
from backend.app.models.group import Group
from backend.app.schemas import GroupCreate
from sqlalchemy import select

async def create_group(
    db: AsyncSession, 
    group: GroupCreate, 
    creator_id: int
) -> Group:
    """Create a new group with eager loading of relationships."""
    # creator_stmt = select(User).where(User.id == creator_id)
    # creator_result = await db.execute(creator_stmt)
    # creator = creator_result.scalar_one()
    result = await db.execute(select(User).where(User.id == creator_id))
    creator = result.scalars().first()

    db_group = Group(
        name=group.name,
        created_by_id=creator_id
    )
    if creator:
        db_group.members.append(creator)
    db.add(db_group)
    await db.commit()
    
    # ✅ CRITICAL: Refresh with eager loading to avoid MissingGreenlet error
    await db.refresh(
        db_group,
        attribute_names=["members", "creator"]
    )
    
    return db_group

async def get_user_groups(
    db: AsyncSession, 
    user_id: int
) -> list[Group]:
    """Get all groups where user is a member, with eager loading."""
    # ✅ Use selectinload to eagerly load the members relationship
    stmt = (
        select(Group)
        .join(Group.members)
        .where(Group.members.any(id=user_id))
        .options(selectinload(Group.members))
        .options(selectinload(Group.creator))
    )
    
    result = await db.execute(stmt)
    groups = result.scalars().all()
    return list(groups)

async def get_group_by_id(
    db: AsyncSession,
    group_id: int
) -> Group | None:
    """Get a group by its ID with eager loading."""
    stmt = (
        select(Group)
        .where(Group.id == group_id)
        .options(selectinload(Group.members))
        .options(selectinload(Group.creator))
    )
    
    result = await db.execute(stmt)
    group = result.scalars().first()
    return group

async def add_member_to_group(
    db: AsyncSession,
    user_id: int,
    group 
) -> Group:
    
    
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    
    if user and user not in group.members:
        group.members.append(user)
        await db.commit()
        
        # ✅ Refresh with eager loading
        await db.refresh(
            group,
            attribute_names=["members", "creator"]
        )
    
    return group

