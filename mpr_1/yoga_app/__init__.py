# yoga_app/__init__.py
from flask import Flask
from yoga_app.config import Config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)

    # Register blueprints
    from yoga_app.routes.main import main_bp
    from yoga_app.routes.video import video_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(video_bp)
    
    with app.app_context():
        db.create_all()
    
    return app