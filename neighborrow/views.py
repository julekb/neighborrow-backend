from flask import current_app as app

from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity
from flask_restful import Resource, reqparse

from .models import db, Item, User, Location


def get_user():
    email = get_jwt_identity()
    return User.query.filter_by(email=email).first()


@app.shell_context_processor
def make_shell_context():
    print('Welcome to (s)hell.')
    return {'db': db, 'User': User, 'Item': Item}


item_parser = reqparse.RequestParser()
item_parser.add_argument('name', required=True)
item_parser.add_argument('price', required=True)


class ItemView(Resource):
    def get(self, id):
        obj = Item.query.filter_by(id=id).one()
        out = {
            "id": obj.id,
            "name": obj.name,
            "owner": obj.owner.id if obj.owner else '',
            "price": obj.price
        }
        return out


class ItemListView(Resource):
    def get(self):
        items = Item.query.all()
        out = [
            {
                "id": item.id,
                "name": item.name,
                "created": str(item.created),
                "modified": str(item.modified),
                "price": item.price,
                "owner": item.owner.first_name if item.owner else ''
            } for item in items
        ]
        return {"items": out}

    @jwt_refresh_token_required
    def post(self, id):
        user = get_user()
        data = item_parser.parse_args()
        obj = Item(**data)
        obj.save_to_db()
        user.items.append(obj)
        user.save_to_db()

        items = Item.query.all()
        out = [
            {
                "id": item.id,
                "name": item.name,
                "owner": item.owner.id if item.owner else '',
                "price": item.price
            } for item in items
        ]
        return {"items": out}


class LocationView(Resource):
    @jwt_refresh_token_required
    def get(self):
        locations = Location.query.all()
        out = [
            {
                "id": location.id,
                "address": location.address
            } for location in locations
        ]
        return out
