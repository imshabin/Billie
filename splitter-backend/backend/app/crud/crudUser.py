# In crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select # Use the modern select statement
from backend.app.models.user import User
from .. import schemas

# Note: async def and await
async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user: schemas.UserCreate, hashed_password: str):
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user