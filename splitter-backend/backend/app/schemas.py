# In schemas.py
from pydantic import BaseModel, EmailStr, ConfigDict,  Field
from typing import List, Optional
from decimal import Decimal


# Schema for creating a new user (expects email and password)
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Schema for reading/returning user data (never include the password)
class User(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

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

# ===================================================================
#                    Expense Members
# ===================================================================

class MemberAdd(BaseModel):
    user_id: int

# ===================================================================
#                     Expense Schemas
# ===================================================================

# Schema for an individual split when reading an expense
class ExpenseSplit(BaseModel):
    owed_by: User
    amount_owed: Decimal

    model_config = ConfigDict(from_attributes=True)

# Schema for the main expense object when reading it
class Expense(BaseModel):
    id: int
    description: str
    amount: Decimal
    paid_by: User
    splits: List[ExpenseSplit]

    model_config = ConfigDict(from_attributes=True)

# Schema for the request body when creating a new expense
class ExpenseCreate(BaseModel):
    description: str = Field(..., min_length=1, max_length=100)
    amount: Decimal = Field(..., gt=0) # Must be greater than 0
    # A list of user IDs to split the expense among
    split_between: List[int] = Field(..., min_items=1)