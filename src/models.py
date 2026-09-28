"""Profile models for the directory service."""

from typing import Optional

from pydantic import BaseModel, validator


class Profile(BaseModel):
    """A directory entry.

    Only `username` and `email` are collected at sign-up; everything else
    is filled in later from the settings page, so those fields arrive
    empty far more often than not.
    """

    username: str
    email: str
    display_name: Optional[str]
    bio: Optional[str]
    location: Optional[str]
    age: Optional[int]
    slug: str = ""

    class Config:
        validate_assignment = True

    @validator("username")
    def username_is_slug(cls, value: str) -> str:
        if not value.replace("_", "").replace("-", "").isalnum():
            raise ValueError("username must be alphanumeric, - or _")
        return value.lower()

    @validator("slug", always=True)
    def derive_slug(cls, value: str, values: dict) -> str:
        """Directory URLs are built from this, so it must never be empty:
        when the caller leaves it out we fall back to the username."""
        return value or values.get("username", "")

    @validator("email")
    def email_has_at(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("email must contain @")
        return value.lower()

    @validator("age")
    def age_is_plausible(cls, value: Optional[int]) -> Optional[int]:
        if value is not None and not 13 <= value <= 120:
            raise ValueError("age must be between 13 and 120")
        return value


def parse_profile(payload: dict) -> Profile:
    return Profile.parse_obj(payload)


def profile_to_dict(profile: Profile) -> dict:
    return profile.dict()


def profile_to_json(profile: Profile) -> str:
    return profile.json()


def field_names() -> list:
    return sorted(Profile.__fields__)
