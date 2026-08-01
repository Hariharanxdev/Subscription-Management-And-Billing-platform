from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository


class AdminUserService:

    # Admin - Get all users
    @staticmethod
    def get_all_users(db: Session):
        return UserRepository.get_all_users(db)

    # Admin - Get one user
    @staticmethod
    def get_user(
        db: Session,
        user_id: int
    ):
        user = UserRepository.get_by_id(
            db,
            user_id
        )

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return user

    # Admin - Deactivate user
    @staticmethod
    def deactivate_user(
        db: Session,
        user_id: int,
        current_admin_id: int
    ):
        user = UserRepository.get_by_id(
            db,
            user_id
        )

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        # Prevent admin from disabling their own account
        if user.id == current_admin_id:
            raise HTTPException(
                status_code=400,
                detail="You cannot deactivate your own admin account."
            )

        # Prevent deactivating another admin
        if user.role == "admin":
            raise HTTPException(
                status_code=403,
                detail="Admin accounts cannot be deactivated."
            )

        if not user.is_active:
            raise HTTPException(
                status_code=400,
                detail="User is already inactive."
            )

        user.is_active = False

        return UserRepository.update_user(
            db,
            user
        )

    # Admin - Activate user
    @staticmethod
    def activate_user(
        db: Session,
        user_id: int
    ):
        user = UserRepository.get_by_id(
            db,
            user_id
        )

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        if user.is_active:
            raise HTTPException(
                status_code=400,
                detail="User is already active."
            )

        user.is_active = True

        return UserRepository.update_user(
            db,
            user
        )