# In auth/router.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession # <-- IMPORT aysnc session
from sqlalchemy.orm import Session

from backend.app import crud, schemas
from backend.app.auth import security
from backend.app.dependencies import get_db 
from backend.app.models.user import User

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

@router.post("/login", response_model=schemas.Token)
async def login_for_access_token(  # 👈 1. Add async here
    db: Session = Depends(get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
):
    # 2. Add await here to get the actual result 👇
    user = await crud.get_user_by_email(db, email=form_data.username)

    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = security.create_access_token(
        data={"sub": user.email}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=schemas.User)
async def read_users_me(
    current_user: User = Depends(security.get_current_user)
):
    """
    Fetches the profile of the currently logged-in user.
    """
    # Because of Depends(get_current_user), this code will only run if the
    # token is valid. The `current_user` variable will be the full
    # user object from the database.
    return current_user