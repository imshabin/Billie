# backend/app/crud.py (or wherever your crudGroup is defined)

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


