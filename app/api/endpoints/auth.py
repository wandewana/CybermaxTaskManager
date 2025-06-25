from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import crud
from app.schemas.user import User, UserCreate, UserLogin
from app.api import deps
from app.core.security import verify_password
from app.core.jwt import create_access_token, create_refresh_token

router = APIRouter()


from fastapi import status
from fastapi.responses import JSONResponse

@router.post(
    "/register",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account. Returns the created user object.",
    tags=["auth"]
)
async def register_user(
    *, 
    db: AsyncSession = Depends(deps.get_db), 
    user_in: UserCreate
) -> User:
    """
    Create a new user account.
    """
    user = await crud.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = await crud.create_user(db, user_in=user_in)
    return user


@router.post(
    "/login",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Login and get tokens",
    description="Authenticate user and return access/refresh tokens.",
    tags=["auth"]
)
async def login(
    *, 
    db: AsyncSession = Depends(deps.get_db), 
    user_data: UserLogin
):
    """
    Authenticate user and return JWT tokens.
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
