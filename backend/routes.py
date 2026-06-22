"""API route handlers (Flask blueprint).

Add routes here and register the blueprint in your application entrypoint.
"""
from flask import Blueprint, jsonify, request

bp = Blueprint('routes', __name__)

@bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@bp.route('/echo', methods=['POST'])
def echo():
    data = request.get_json(silent=True) or {}
    return jsonify({'received': data})
