"""Authentication helpers and decorators.

This file contains simple examples; adapt to your auth method (JWT, OAuth, etc.).
"""
from functools import wraps
from flask import request, jsonify

# Example decorator for simple token check
def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            return jsonify({'error': 'missing token'}), 401
        token = auth.split(' ', 1)[1]
        # Replace this with real verification
        if token != 'secret-token':
            return jsonify({'error': 'invalid token'}), 401
        return f(*args, **kwargs)
    return wrapper
