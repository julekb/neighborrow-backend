import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(os.environ['APP_SETTINGS'])
    db.init_app(app)
    migrate = Migrate(app, db)    
    login_manager = LoginManager()


    with app.app_context():
        from . import routes

        # db.create_all()
        return app
