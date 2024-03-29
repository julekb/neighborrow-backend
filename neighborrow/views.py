from flask import current_app as app
from flask import request

from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity
from flask_restful import Resource

from .models import db, Item, User, Location
from .schemas import UserSchema, ItemSchema, LocationSchema


def get_user():
    email = get_jwt_identity()
    return User.query.filter_by(email=email).first()


@app.shell_context_processor
def make_shell_context():
    print('Welcome to (s)hell.')
    return {'db': db, 'User': User, 'Item': Item, 'Location': Location}


class UserSelfView(Resource):
    @jwt_refresh_token_required
    def get(self):
        user = get_user()
        return UserSchema().dump(user)


class ItemView(Resource):
    def get(self, id):
        obj = Item.query.filter_by(id=id).one()
        out = ItemSchema().dump(obj)
        return out


class ItemListView(Resource):
    def get(self):
        items = Item.query.all()
        out = ItemSchema(many=True).dump(items)
        return out

    @jwt_refresh_token_required
    def post(self):
        user = get_user()
        schema = ItemSchema()
        data = request.get_json(force=True)
        obj = schema.load(data).save_to_db()
        user.items.append(obj)
        user.save_to_db()

        out = schema.dump(obj)
        return out


class LocationView(Resource):
    def get(self):
        data = request.get_json(force=True)
        if 'lat' in data and 'lon' in data:
            locations = Location.get_in_range(lat=data['lat'], lon=data['lon'])
        else:
            locations = Location.query.all()
        out = LocationSchema(many=True).dump(locations)
        return out

    def post(self):
        data = request.get_json(force=True)
        schema = LocationSchema()
        obj = schema.load(data).save_to_db()

        out = LocationSchema().dump(obj)
        return out


class LocationDetailView(Resource):
    def get(self, id):
        obj = Location.query.filter_by(id=id).one()
        return LocationSchema().dump(obj)
