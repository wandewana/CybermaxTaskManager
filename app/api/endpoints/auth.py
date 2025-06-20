from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import crud
from app.schemas.user import User, UserCreate, UserLogin
from app.api import deps
from app.core.security import verify_password
from app.core.jwt import create_access_token, create_refresh_token

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


@router.post("/login")
async def login(
    *, 
    db: AsyncSession = Depends(deps.get_db), 
    user_data: UserLogin
):
    """
    Authenticate user and return tokens.
    """
    user = await crud.get_user_by_email(db, email=user_data.email)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
