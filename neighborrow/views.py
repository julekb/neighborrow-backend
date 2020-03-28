from flask import current_app as app
from flask import request

from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity
from flask_restful import Resource, reqparse

from .models import db, Item, User


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
    @jwt_refresh_token_required
    def post(self):
        user = get_user()
        data = item_parser.parse_args()
        obj = Item(**data)
        obj.save_to_db()

        items = Item.query.all()
        out = [
            {
                "pk": item.id,
                "name": item.name,
                "price": item.price
            } for item in items
        ]
        return {"items": out}

    def get(self):
        items = Item.query.all()
        out = [
            {
                "pk": item.id,
                "name": item.name,
                "price": item.price,
                "owner": item.owner.first_name if item.owner else ''
            } for item in items
        ]
        return {"items": out}
