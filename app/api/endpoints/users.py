from fastapi import APIRouter, Depends

from app.models.user import User
from app.schemas.user import User as UserSchema
from app.api import deps

router = APIRouter()


@router.get("/me", response_model=UserSchema)
async def read_users_me(
    current_user: User = Depends(deps.get_current_user)
):
    """
    Fetch the current logged in user.
    """
    return current_user
