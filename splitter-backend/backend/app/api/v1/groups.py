# In backend/app/api/v1/groups.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession # Use AsyncSession for type hint
from backend.app.dependencies import get_db
from backend.app.auth.security import get_current_user
from backend.app.schemas import User
from backend.app.schemas import Group, GroupCreate
from backend.app.schemas import MemberAdd

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

@router.get("/{group_id}", response_model=Group)
async def get_group_details(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve details for a specific group, including its members.
    """
    
    group = await crudGroup.get_group_by_id(db=db, group_id=group_id)

    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

    # Security check: ensure the current user is a member of the group they are trying to view
    if current_user not in group.members:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this group")

    return group

# Endpoint 3: Add a member to a group
@router.post("/{group_id}/members", response_model=Group)
async def add_member_to_group(
    group_id: int,
    member_request: MemberAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Add a new user to a group.
    """
    
    group = await crudGroup.get_group_by_id(db=db, group_id=group_id)
    add_members = await crudGroup.add_member_to_group(
        db=db,
        user_id=member_request.user_id,
        group=group)
    
    return add_members