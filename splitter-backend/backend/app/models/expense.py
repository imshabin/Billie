from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from .base import Base
from .bridge_tables import user_group_association 
# ... Your User, Group, and group_members_association table definitions ...

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    # Use Numeric for currency to avoid floating-point errors
    amount = Column(Numeric(10, 2), nullable=False)

    group_id = Column(Integer, ForeignKey('groups.id'))
    paid_by_id = Column(Integer, ForeignKey('users.id'))

    # Relationships
    group = relationship("Group")
    paid_by = relationship("User")
    splits = relationship("ExpenseSplit", back_populates="expense", cascade="all, delete-orphan")

class ExpenseSplit(Base):
    __tablename__ = 'expense_splits'
    id = Column(Integer, primary_key=True, index=True)
    amount_owed = Column(Numeric(10, 2), nullable=False)

    expense_id = Column(Integer, ForeignKey('expenses.id'))
    owed_by_id = Column(Integer, ForeignKey('users.id'))

    # Relationships
    expense = relationship("Expense", back_populates="splits")
    owed_by = relationship("User")