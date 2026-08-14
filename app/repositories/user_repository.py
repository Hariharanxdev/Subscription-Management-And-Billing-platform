from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    # Get user by email
    @staticmethod
    def get_by_email(
        db: Session,
        email: str
    ):
        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    # Get user by username
    @staticmethod
    def get_by_username(
        db: Session,
        username: str
    ):
        return (
            db.query(User)
            .filter(User.username == username)
            .first()
        )

    # Get user by ID
    @staticmethod
    def get_by_id(
        db: Session,
        user_id: int
    ):
        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    # Create user
    @staticmethod
    def create(
        db: Session,
        user: User
    ):
        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    # Admin - Get all users
    @staticmethod
    def get_all_users(
        db: Session
    ):
        return (
            db.query(User)
            .order_by(User.id.asc())
            .all()
        )

    # Admin - Update user
    @staticmethod
    def update_user(
        db: Session,
        user: User
    ):
        db.commit()
        db.refresh(user)

        return user

    # Customer - Update profile
    @staticmethod
    def update_profile(
        db: Session,
        user_id: int,
        profile_data: dict
    ):
        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:
            return None

        for field, value in profile_data.items():
            if hasattr(user, field):
                setattr(user, field, value)

        db.commit()
        db.refresh(user)

        return user