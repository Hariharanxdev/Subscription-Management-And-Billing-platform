'''from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
import traceback
from app.schemas.user import UserCreate, UserLogin


class AuthService:

    @staticmethod
    def register(db: Session, user_data: UserCreate):
        if UserRepository.get_by_email(db, user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        if UserRepository.get_by_username(db, user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )

        # compute hash first to make errors visible here
        try:
            hashed = hash_password(user_data.password)
        except Exception as e:
            tb = traceback.format_exc()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=tb)
        print(f"[DEBUG] hashed password for {user_data.email}: {hashed[:40]}")

        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed,
        )

        return UserRepository.create(db, user)

    """@staticmethod
    def login(db: Session, form_data: OAuth2PasswordRequestForm):
        user = UserRepository.get_by_email(db, form_data.username)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        token = create_access_token(
            {
                "sub": user.email,
                "role": user.role,
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }"""

    @staticmethod
    def login(
        db: Session,
        form_data: OAuth2PasswordRequestForm
    ):
        user = UserRepository.get_by_email(
            db,
            form_data.username
        )

        # Check whether user exists
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        # Verify password
        if not verify_password(
            form_data.password,
            user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        # Block inactive users
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "Your account is inactive. "
                    "Please contact the administrator."
                ),
            )

        # Create JWT only for active users
        token = create_access_token(
            {
                "sub": user.email,
                "role": user.role,
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }'''

import logging

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.services.email_service import EmailService


logger = logging.getLogger(__name__)


class AuthService:

    @staticmethod
    def register(
        db: Session,
        user_data: UserCreate
    ):
        # Check duplicate email
        if UserRepository.get_by_email(
            db,
            user_data.email
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Check duplicate username
        if UserRepository.get_by_username(
            db,
            user_data.username
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )

        # Hash password
        try:
            hashed = hash_password(
                user_data.password
            )
        except Exception:
            logger.exception(
                "Password hashing failed for %s",
                user_data.email
            )

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to create account.",
            )

        # Create user
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed,
        )

        # Save user to database
        created_user = UserRepository.create(
            db,
            user
        )

        # Send welcome email
        # Email failure should NOT fail registration.
        try:
            email_sent = EmailService.send_welcome_email(
                to_email=created_user.email,
                username=created_user.username,
            )

            if email_sent:
                logger.info(
                    "Welcome email sent to %s",
                    created_user.email
                )
            else:
                logger.warning(
                    "Welcome email could not be sent to %s",
                    created_user.email
                )

        except Exception:
            logger.exception(
                "Unexpected error while sending welcome email to %s",
                created_user.email
            )

        return created_user

    @staticmethod
    def login(
        db: Session,
        form_data: OAuth2PasswordRequestForm
    ):
        user = UserRepository.get_by_email(
            db,
            form_data.username
        )

        # Check whether user exists
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        # Verify password
        if not verify_password(
            form_data.password,
            user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        # Block inactive users
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "Your account is inactive. "
                    "Please contact the administrator."
                ),
            )

        # Create JWT only for active users
        token = create_access_token(
            {
                "sub": user.email,
                "role": user.role,
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }