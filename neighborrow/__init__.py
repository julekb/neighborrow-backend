import os

from flask import Flask

from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restful import Api


db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    api = Api(app)

    app.config.from_object(os.environ['APP_SETTINGS'])
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager = LoginManager()
    jtw = JWTManager(app)

    with app.app_context():
        from . import auth
        from . import routes
        # db.create_all()
        users_prefix = '/users'
        api.add_resource(auth.UserSignUp, users_prefix + '/signup')
        api.add_resource(auth.UserLogin, users_prefix + '/login')
        api.add_resource(auth.UserLogoutAccess, users_prefix + '/logout/access')
        api.add_resource(auth.UserLogoutRefresh, users_prefix + '/logout/refresh')
        api.add_resource(auth.TokenRefresh, users_prefix + '/token/refresh')
        api.add_resource(auth.SecretResource, users_prefix + '/secret')
        return app
