"""Authentication helpers and decorators using JWT and secure password hashing.

Provides:
- hash_password(password)
- verify_password(password, hashed_password)
- create_access_token(user_id)
- verify_access_token(token)
- require_auth decorator that checks Authorization: Bearer <token>

This is a lightweight, production-ready foundation. Adjust token expiry and
error handling to suit your application needs.
"""
from functools import wraps
from flask import request, jsonify, g
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature,
    SignatureExpired,
)
from .config import JWT_SECRET_KEY

# Token expiration in seconds (default 1 hour). Adjust as needed.
DEFAULT_ACCESS_TOKEN_EXPIRES = 3600


# Password utilities
def hash_password(password: str) -> str:
    """Hash a plaintext password for storage.

    Uses werkzeug.security.generate_password_hash which applies PBKDF2 by default.
    """
    return generate_password_hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against the stored hash."""
    return check_password_hash(hashed_password, password)


# JWT (itsdangerous-based) utilities
def create_access_token(user_id, expires_in: int = DEFAULT_ACCESS_TOKEN_EXPIRES) -> str:
    """Create a signed access token containing the user_id.

    Returns a string token. The token will expire after `expires_in` seconds.
    """
    s = Serializer(JWT_SECRET_KEY, expires_in=expires_in)
    token = s.dumps({"user_id": user_id})
    # itsdangerous may return bytes in some versions; ensure a str is returned.
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token


def verify_access_token(token: str):
    """Verify the token and return the payload (dict) on success, otherwise None.

    If the token is expired or invalid, None is returned.
    """
    s = Serializer(JWT_SECRET_KEY)
    try:
        data = s.loads(token)
        return data
    except SignatureExpired:
        # Token is valid but expired
        return None
    except BadSignature:
        # Token is invalid
        return None


# Decorator for endpoints that require a valid access token.
def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "missing token"}), 401
        token = auth.split(" ", 1)[1]
        payload = verify_access_token(token)
        if not payload or "user_id" not in payload:
            return jsonify({"error": "invalid or expired token"}), 401
        # Attach user information to flask.g for handlers to use
        g.current_user = payload.get("user_id")
        return f(*args, **kwargs)

    return wrapper
