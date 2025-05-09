from flask import Flask
from .config import Config
from .database import db
from .routes.user import user_bp
from .routes.code import code_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(code_bp, url_prefix='/api')

    with app.app_context():
        db.drop_all()
        db.create_all()

    return app
