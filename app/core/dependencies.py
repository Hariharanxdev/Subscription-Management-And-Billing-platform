from fastapi import Depends, HTTPException, status

from app.core.security import get_current_user


def get_current_admin(current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can perform this action."
        )

    return current_user