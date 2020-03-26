from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask_restful import Resource, reqparse

from .models import User, RevokedToken


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
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti=jti)
            revoked_token.save_to_db()
            return {'message': 'Access token has been revoked.'}
        except:
            return {'message': 'Something went wrong.'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti=jti)
            revoked_token.save_to_db()
            return {'message': 'Refresh token has been revoked.'}
        except:
            return {'message': 'Something went wrong.'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        user = get_jwt_identity()
        access_token = create_access_token(identity=user)
        return {'access_token': access_token}
