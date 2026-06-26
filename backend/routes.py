"""API route handlers (Flask blueprint).

Add routes here and register the blueprint in your application entrypoint.
"""
from datetime import datetime
from flask import Blueprint, jsonify, request, g

from .database import SessionLocal
from .models import User
from .auth import hash_password, verify_password, create_access_token, require_auth

bp = Blueprint('routes', __name__)

@bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@bp.route('/echo', methods=['POST'])
def echo():
    data = request.get_json(silent=True) or {}
    return jsonify({'received': data})


@bp.route('/api/register', methods=['POST'])
def register():
    """Register a new user and return an access token.

    Expected JSON body: {"username": "...", "password": "..."}
    Returns: {"access_token": "..."}
    """
    data = request.get_json(silent=True) or {}
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''

    if not username or not password:
        return jsonify({'error': 'username and password are required'}), 400

    db = SessionLocal()
    try:
        # Check for existing user
        if db.query(User).filter_by(username=username).first():
            return jsonify({'error': 'username already taken'}), 400

        # Create and persist user using ORM model instance
        hashed = hash_password(password)
        user = User(username=username, password=hashed, created_at=datetime.utcnow().isoformat())
        db.add(user)
        db.commit()
        db.refresh(user)

        token = create_access_token(user.id)
        return jsonify({'access_token': token})
    finally:
        db.close()


@bp.route('/api/login', methods=['POST'])
def login():
    """Authenticate a user and return an access token.

    Expected JSON body: {"username": "...", "password": "..."}
    Returns: {"access_token": "..."}
    """
    data = request.get_json(silent=True) or {}
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''

    if not username or not password:
        return jsonify({'error': 'username and password are required'}), 400

    db = SessionLocal()
    try:
        user = db.query(User).filter_by(username=username).first()
        if not user or not verify_password(password, user.password):
            return jsonify({'error': 'invalid credentials'}), 401

        token = create_access_token(user.id)
        return jsonify({'access_token': token})
    finally:
        db.close()


@bp.route('/api/me', methods=['GET'])
@require_auth
def me():
    """Return current authenticated user's profile.

    Protected by require_auth which sets g.current_user to the user id.
    """
    user_id = getattr(g, 'current_user', None)
    if not user_id:
        return jsonify({'error': 'not authenticated'}), 401

    db = SessionLocal()
    try:
        user = db.query(User).get(user_id)
        if not user:
            return jsonify({'error': 'user not found'}), 404

        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'is_active': user.is_active,
            'created_at': user.created_at,
            'last_login': user.last_login,
        })
    finally:
        db.close()


@bp.route('/api/profile', methods=['PUT'])
@require_auth
def update_profile():
    """Update current authenticated user's profile (username and email).

    Protected endpoint. Accepts JSON with optional 'username' and 'email'.
    Rejects duplicates. Returns the updated user profile.
    """
    data = request.get_json(silent=True) or {}
    new_username = (data.get('username') or '').strip() or None
    new_email = (data.get('email') or '').strip() or None

    if new_username is None and new_email is None:
        return jsonify({'error': 'nothing to update'}), 400

    user_id = getattr(g, 'current_user', None)
    if not user_id:
        return jsonify({'error': 'not authenticated'}), 401

    db = SessionLocal()
    try:
        user = db.query(User).get(user_id)
        if not user:
            return jsonify({'error': 'user not found'}), 404

        # Check duplicates for username
        if new_username and new_username != user.username:
            if db.query(User).filter(User.username == new_username).first():
                return jsonify({'error': 'username already taken'}), 400
            user.username = new_username

        # Check duplicates for email
        if new_email and new_email != user.email:
            if db.query(User).filter(User.email == new_email).first():
                return jsonify({'error': 'email already taken'}), 400
            user.email = new_email

        db.commit()
        db.refresh(user)

        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'is_active': user.is_active,
        })
    finally:
        db.close()
