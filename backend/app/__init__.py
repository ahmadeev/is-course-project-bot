from flask import Flask
from .config import Config
from .database import db
from .routes.user import user_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(user_bp, url_prefix='/api')

    with app.app_context():
        db.create_all()

    return app
