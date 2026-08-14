from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.schemas.profile import ProfileUpdate


class ProfileService:

    @staticmethod
    def get_profile(
        db: Session,
        user_id: int
    ):
        user = UserRepository.get_by_id(
            db,
            user_id
        )

        if not user:
            raise ValueError("User not found")

        return user

    @staticmethod
    def update_profile(
        db: Session,
        user_id: int,
        profile_data: ProfileUpdate
    ):
        user = UserRepository.get_by_id(
            db,
            user_id
        )

        if not user:
            raise ValueError("User not found")

        update_data = profile_data.model_dump(
            exclude_unset=True
        )

        if not update_data:
            return user

        # Prevent profile update from changing protected fields.
        protected_fields = {
            "id",
            "email",
            "hashed_password",
            "role",
            "is_active",
            "created_at",
            "updated_at",
        }

        update_data = {
            field: value
            for field, value in update_data.items()
            if field not in protected_fields
        }

        return UserRepository.update_profile(
            db,
            user_id,
            update_data
        )