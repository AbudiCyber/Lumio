"""Middleware examples.

Provide WSGI middleware or Flask before/after request handlers here.
"""
from flask import request

# WSGI-style middleware wrapper
def simple_middleware(app):
    def middleware(environ, start_response):
        # Example: you could log or set env values here
        return app(environ, start_response)
    return middleware

# Flask-style request hooks
def before_request():
    # Example hook: populate request context or perform logging
    pass

def after_request(response):
    # Example: modify response headers
    response.headers['X-Backend'] = 'Lumio'
    return response
