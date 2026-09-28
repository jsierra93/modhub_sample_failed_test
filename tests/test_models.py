import pytest
from pydantic import ValidationError

from src.models import (
    Profile,
    field_names,
    parse_profile,
    profile_to_dict,
    profile_to_json,
)

FULL = {
    "username": "ada",
    "email": "ada@example.com",
    "display_name": "Ada Lovelace",
    "bio": "Analytical engine enthusiast",
    "location": "London",
    "age": 36,
    "slug": "ada-lovelace",
}


def test_full_profile_round_trips():
    profile = parse_profile(FULL)
    assert profile.username == "ada"
    assert profile.display_name == "Ada Lovelace"


def test_signup_only_supplies_username_and_email():
    """The sign-up form posts exactly these two fields; everything else is
    filled in later from the settings page."""
    profile = Profile(username="grace", email="grace@example.com")
    assert profile.username == "grace"
    assert profile.display_name is None
    assert profile.age is None


def test_username_is_lowercased():
    assert Profile(username="ADA", email="a@b.com").username == "ada"


def test_email_is_lowercased():
    assert Profile(username="ada", email="ADA@Example.COM").email == "ada@example.com"


def test_username_rejects_spaces():
    with pytest.raises(ValidationError):
        Profile(username="ada lovelace", email="a@b.com")


def test_email_requires_at():
    with pytest.raises(ValidationError):
        Profile(username="ada", email="not-an-email")


def test_age_rejects_children():
    with pytest.raises(ValidationError):
        Profile(username="ada", email="a@b.com", age=4)


def test_age_rejects_implausible():
    with pytest.raises(ValidationError):
        Profile(username="ada", email="a@b.com", age=200)


def test_age_accepts_none():
    assert Profile(username="ada", email="a@b.com", age=None).age is None


def test_to_dict_keeps_every_field():
    assert set(profile_to_dict(parse_profile(FULL))) == set(FULL)


def test_slug_defaults_to_the_username():
    """Directory URLs are built from the slug, so an omitted slug must fall
    back to the username rather than staying empty."""
    assert Profile(username="Grace", email="g@example.com").slug == "grace"


def test_explicit_slug_is_kept():
    assert parse_profile(FULL).slug == "ada-lovelace"


def test_to_json_uses_the_documented_wire_format():
    """Downstream consumers parse this with a fixed-format reader."""
    assert '"username": "ada"' in profile_to_json(parse_profile(FULL))


def test_field_names_are_stable():
    assert field_names() == [
        "age",
        "bio",
        "display_name",
        "email",
        "location",
        "slug",
        "username",
    ]


def test_assignment_is_validated():
    profile = Profile(username="ada", email="a@b.com")
    with pytest.raises(ValidationError):
        profile.email = "nope"
