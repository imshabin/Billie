from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .base import Base
from .bridge_tables import user_group_association  # Import the Base object


class Group(Base):
    __tablename__ = 'groups'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    created_by_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # ✅ Use lazy="selectin" for async compatibility
    creator = relationship(
        "User",
        lazy="selectin"
    )
    
    # ✅ Use lazy="selectin" to prevent MissingGreenlet errors
    # This tells SQLAlchemy to load members in a separate SELECT automatically
    members = relationship(
        "User",
        secondary=user_group_association,
        back_populates="groups",
        lazy="selectin"  # ← Critical for async operations
    )

    
# pip install pydantic[email]
# pip install passlib