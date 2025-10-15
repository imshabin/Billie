# In auth/router.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession # <-- IMPORT aysnc session

from backend.app import crud, schemas
from backend.app.auth import security
from backend.app.dependencies import get_db # <-- Assumes your get_db is in a dependencies.py file

router = APIRouter()

@router.post("/register", response_model=schemas.User)
# Note: async def, AsyncSession, and await
async def register_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_email(db, email=user.email) # <-- AWAIT
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    print(f"Password received by server: '{user.password}'")
    hashed_password = security.get_password_hash(user.password)
    # The create function must also be awaited
    return await crud.create_user(db=db, user=user, hashed_password=hashed_password) # <-- AWAIT