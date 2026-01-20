from flask import Flask
from config import Config


def create_app(config_class=Config):
    app = Flask(
        __name__, template_folder="../templates"
    )  # Point to the root templates folder
    app.config.from_object(config_class)

    # Register Blueprints
    from app.routes.main import main_bp
    from app.routes.api import api_bp
    from app.routes.publish import publish_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(publish_bp)

    return app
