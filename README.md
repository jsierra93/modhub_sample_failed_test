# profile-directory

A small library of profile models for an internal directory service.

Two fields are collected at sign-up — `username` and `email`. Everything
else (`display_name`, `bio`, `location`, `age`) is filled in later from the
settings page, so profiles routinely exist with those left empty.

## Usage

```python
from src.models import Profile, parse_profile

Profile(username="grace", email="grace@example.com")
parse_profile({"username": "ada", "email": "ada@example.com", "age": 36})
```

## Development

```
pip install -r requirements.txt
pytest
ruff check .
```

## Status

Still on Pydantic v1. The pin in `requirements.txt` has not been revisited
since the project was written.
