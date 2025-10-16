# In models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base
from .bridge_tables import user_group_association  # Import the association table


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String, unique=True, index=True)
    role_id = Column(Integer)
    created_at = Column(String)

    groups = relationship("Group", secondary=user_group_association, back_populates="members")

# pip install pydantic[email]
# pip install passlib