# In schemas.py
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional

# Schema for creating a new user (expects email and password)
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Schema for reading/returning user data (never include the password)
class User(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True # Helps Pydantic work with SQLAlchemy objects

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: EmailStr | None = None

# ===================================================================
#                      Group Schemas
# ===================================================================

# Shared properties for a group
class GroupBase(BaseModel):
    name: str

# Properties required to create a new group
class GroupCreate(GroupBase):
    pass

class Group(GroupBase):
    id: int
    created_by_id: int
    members: List[User] = []
    
    # ✅ Updated for Pydantic v2
    model_config = ConfigDict(from_attributes=True)
