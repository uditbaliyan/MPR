# yoga_app/__init__.py
from flask import Flask
from yoga_app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register blueprints
    from yoga_app.routes.main import main_bp
    from yoga_app.routes.video import video_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(video_bp)

    return app