# from flask import Blueprint
from flask import current_app as app

from flask_restful import Api

from .auth import UserSignUpView, UserLoginView, UserLogoutAccessView, UserLogoutRefreshView, TokenRefreshView, LocationView
from .views import ItemView

api = Api(app)

users_prefix = '/users'
api.add_resource(UserSignUpView, users_prefix + '/signup')
api.add_resource(UserLoginView, users_prefix + '/login')
api.add_resource(UserLogoutAccessView, users_prefix + '/logout-access')
api.add_resource(UserLogoutRefreshView, users_prefix + '/logout-refresh')
api.add_resource(TokenRefreshView, users_prefix + '/refresh-token')

items_prefix = '/items'
api.add_resource(ItemView, items_prefix + '')

locations_prefix = '/locations'
api.add_resource(LocationView, users_prefix + '')
