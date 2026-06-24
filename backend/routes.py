"""API route handlers (Flask blueprint).

Add routes here and register the blueprint in your application entrypoint.
"""
from datetime import datetime
from flask import Blueprint, jsonify, request

from .database import SessionLocal
from .models import User
from .auth import hash_password, verify_password, create_access_token

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
