import os

from flask import Flask

from flask_admin import Admin
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
ma = Marshmallow()


def create_app():
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object(os.environ['APP_SETTINGS'])
    db.init_app(app)
    migrate = Migrate(app, db)

    admin_panel = Admin(app, name='Neighborrow', template_mode='bootstrap3')
    # from .admin import UserAdmin
    # admin_panel.add_view(UserAdmin(db.session))
    # admin.add_view(ItemAdmin)
    # admin.add_view(LocationAdmin)

    ma.init_app(app)
    # login_manager = LoginManager()
    jwt = JWTManager(app)
    from .models import RevokedToken

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return RevokedToken.is_jti_blacklisted(jti)

    with app.app_context():
        from . import routes, commands

        return app
