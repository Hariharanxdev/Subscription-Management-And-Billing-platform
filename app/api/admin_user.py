from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.schemas.admin_user import AdminUserResponse
from app.services.admin_user_service import AdminUserService
from app.core.dependencies import get_current_admin


router = APIRouter(
    prefix="/admin/users",
    tags=["Admin - User Management"]
)


# Admin - View all users
@router.get(
    "/",
    response_model=list[AdminUserResponse]
)
def get_all_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    return AdminUserService.get_all_users(db)


# Admin - View one user
@router.get(
    "/{user_id}",
    response_model=AdminUserResponse
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    return AdminUserService.get_user(
        db,
        user_id
    )


# Admin - Deactivate user
@router.put(
    "/{user_id}/deactivate",
    response_model=AdminUserResponse
)
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    return AdminUserService.deactivate_user(
        db,
        user_id,
        current_admin.id
    )


# Admin - Activate user
@router.put(
    "/{user_id}/activate",
    response_model=AdminUserResponse
)
def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    return AdminUserService.activate_user(
        db,
        user_id
    )