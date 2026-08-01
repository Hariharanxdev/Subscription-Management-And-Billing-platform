from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

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
    def get_all_users(db: Session):
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