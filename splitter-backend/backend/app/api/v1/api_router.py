# In backend/app/api/v1/api_router.py

from fastapi import APIRouter
from . import health, groups  # Import your route modules from the same directory
from . import expenses
api_router = APIRouter()

# Include the health check router
# This makes its endpoints available at the root of the api_router
api_router.include_router(health.router, tags=["Health"])

# Include the groups router
# This adds all endpoints from groups.py under the "/groups" prefix
api_router.include_router(groups.router, prefix="/groups", tags=["Groups"])
api_router.include_router(expenses.router, tags=["Expenses"])

# When you create the expenses router, you will add it here later:
# from . import expenses
# api_router.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])