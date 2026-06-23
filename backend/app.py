"""Flask application bootstrap for the Lumio backend.

- Creates a Flask app
- Registers routes blueprint
- Initializes the database
- Registers middleware hooks
"""
from flask import Flask, jsonify

# Import local modules
from .routes import bp as routes_bp
from .database import init_db
from .middleware import before_request, after_request


def create_app(config_overrides=None):
    app = Flask(__name__)

    # Apply any config overrides (dict) for tests or runtime
    if config_overrides:
        app.config.update(config_overrides)

    # Initialize database (creates tables if needed)
    init_db()

    # Register middleware hooks if provided
    app.before_request(before_request)
    app.after_request(after_request)

    # Register blueprints
    app.register_blueprint(routes_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return jsonify({
            'message': 'Lumio Backend Running'
        })

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000)
