# from flask import Blueprint
from flask import current_app as app
from flask import request

from .models import db, Item, User


@app.shell_context_processor
def make_shell_context():
    print('Welcome to (s)hell.')
    return {'db': db, 'User': User, 'Item': Item}


items_prefix = '/items'


@app.route(items_prefix, methods=['GET', 'POST', 'DELETE'])
def items():
    if request.method == 'GET':
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

    elif request.method == 'POST':
        data = request.get_json()
        obj = Item(name=data['name'], price=data['price'])
        db.session.add(obj)
        db.session.commit()

        items = Item.query.all()
        out = [
            {
                "pk": item.id,
                "name": item.name,
                "price": item.price
            } for item in items
        ]
        return {"items": out}

    elif request.method == 'DELETE':
        id = request.get_json()['id']
        item = Item.query.get(id)
        db.session.delete(item)
        db.session.commit()
        return f"Item {id} deleted."
