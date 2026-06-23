# Configuration Settings

# Environment-based configuration with safe defaults.
import os

# Secret key used by the application (change in production).
SECRET_KEY = os.getenv("SECRET_KEY", "change-me")

# JWT secret key; defaults to SECRET_KEY when not explicitly set.
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)

# Database connection URL; default to a local SQLite file for dev/testing.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")


def _str_to_bool(value: str) -> bool:
    """Convert a string environment value to boolean.

    Interprets "1", "true", "yes", "on" (case-insensitive) as True.
    Everything else is False.
    """
    return str(value).strip().lower() in ("1", "true", "yes", "on")

# Debug flag parsed from environment.
DEBUG = _str_to_bool(os.getenv("DEBUG", "False"))
