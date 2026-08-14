from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class ProfileResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    phone_number: str | None = None

    address_line1: str | None = None
    address_line2: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    pincode: str | None = None

    profile_image: str | None = None

    role: str
    is_active: bool

    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class ProfileUpdate(BaseModel):
    username: str | None = None
    phone_number: str | None = None

    address_line1: str | None = None
    address_line2: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    pincode: str | None = None