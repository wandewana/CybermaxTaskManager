from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import crud
from app.schemas.user import User, UserCreate
from app.api import deps

router = APIRouter()


@router.post("/register", response_model=User)
async def register_user(
    *, 
    db: AsyncSession = Depends(deps.get_db), 
    user_in: UserCreate
) -> User:
    """
    Create new user.
    """
    user = await crud.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = await crud.create_user(db, user_in=user_in)
    return user
