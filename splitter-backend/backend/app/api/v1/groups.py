# In backend/app/api/v1/groups.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession # Use AsyncSession for type hint
from backend.app.dependencies import get_db
from backend.app.auth.security import get_current_user
from backend.app.schemas import User
from backend.app.schemas import Group, GroupCreate
from backend.app.crud import crudGroup

router = APIRouter()

@router.post("/", response_model=Group, status_code=201)
async def handle_create_group(
    *,
    db: AsyncSession = Depends(get_db), # Correct type hint
    group_in: GroupCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Create a new group.
    """
    # ✅ Add 'await' here to get the actual group object
    group = await crudGroup.create_group(db=db, group=group_in, creator_id=current_user.id)
    return group

@router.get("/", response_model=List[Group])
async def handle_get_user_groups(
    *,
    db: AsyncSession = Depends(get_db), # Correct type hint
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve all groups for the current user.
    """
    # ✅ Add 'await' here as well
    groups = await crudGroup.get_user_groups(db=db, user_id=current_user.id)
    return groups