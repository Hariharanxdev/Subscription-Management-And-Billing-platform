from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.profile import ProfileResponse, ProfileUpdate
from app.services.profile_service import ProfileService
from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


@router.get(
    "",
    response_model=ProfileResponse
)
def get_profile(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        return ProfileService.get_profile(
            db,
            current_user.id
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc)
        )


@router.put(
    "",
    response_model=ProfileResponse
)
def update_profile(
    profile_data: ProfileUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        return ProfileService.update_profile(
            db,
            current_user.id,
            profile_data
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc)
        )