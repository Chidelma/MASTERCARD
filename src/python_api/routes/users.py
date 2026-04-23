from fastapi import APIRouter, HTTPException, status

from python_api.db.database import SessionDep
from python_api.db.schemas import User
from python_api.models import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: SessionDep) -> UserResponse:
    """
    Create a new user with the given details.
    Returns the created user's ID and details.
    """
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        home_address=user.home_address,
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user",
        ) from e

    return UserResponse.model_validate(db_user)
