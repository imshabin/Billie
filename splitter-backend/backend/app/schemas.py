# In schemas.py

from pydantic import BaseModel, EmailStr

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