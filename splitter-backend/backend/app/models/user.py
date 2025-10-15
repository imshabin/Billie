# In models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()  # ✅ create the Base object


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String, unique=True, index=True)
    role_id = Column(Integer)
    created_at = Column(String)

# pip install pydantic[email]
# pip install passlib