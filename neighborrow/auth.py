from flask import current_app as app
from flask import request

from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask_restful import Resource, reqparse

from . import db
from .models import User


signup_parser = reqparse.RequestParser()
signup_parser.add_argument('first_name', required=False)
signup_parser.add_argument('last_name', required=False)
signup_parser.add_argument('email', help='This field annot be blank.', required=True)
signup_parser.add_argument('password', help='This field cannot be blank.', required=True)

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', help='This field annot be blank.', required=True)
login_parser.add_argument('password', help='This field cannot be blank.', required=True)


class UserSignUp(Resource):
    def post(self):
        data = signup_parser.parse_args()
        password = data.pop('password')
        user = User(**data, password=User.generate_hash(password))

        try:
            user.save_to_db()
            access_token = create_access_token(identity=data['email'])
            refresh_token = create_refresh_token(identity=data['email'])
            return {
                'message': 'Logged in as {} {}'.format(user.first_name, user.last_name),
                'access_token': access_token,
                'refresh_token': refresh_token
            }

        except Exception as e:
            return 'Ups, something went wrong. ()'.format(str(e)), 500


class UserLogin(Resource):
    def post(self):
        data = login_parser.parse_args()
        user = User.query.filter_by(email=data['email']).first()

        if not user:
            return 'User does not exist.'

        if User.verify_hash(data['password'], user.password):
            access_token = create_access_token(identity=data['email'])
            refresh_token = create_refresh_token(identity=data['email'])
            return {
                'message': 'Logged in as {} {}'.format(user.first_name, user.last_name),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        return 'Incorrect password.'


class UserLogoutAccess(Resource):
    def post(self):
        return {'message': 'User logout'}


class UserLogoutRefresh(Resource):
    def post(self):
        return {'message': 'User logout'}


class TokenRefresh(Resource):
    def post(self):
        return {'message': 'Token refresh'}


class SecretResource(Resource):
    def get(self):
        return {
            'answer': 42
        }
# class UserSignupView(Resource)
# def get(self):
#         return
#
# class LoginView(Resource):
#     def post(self):
#         first_name = request.json.get('first_name')
#         last_name = request.json.get('last_name')
#         email = request.json.get('email')
#         password = request.json.get('password')
#         phone = request.json.get('password')
#
#         if not (first_name or last_name or password or phone or email):
#             raise
#
#         user = User(first_name=first_name, last_name=last_name, email=email, phone=phone)
#         user.set_password(password)
#         db.session.add(user)
#         db.session.commit()
