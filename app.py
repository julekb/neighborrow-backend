import os

from flask import Flask
from flask import request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # signals
app.run(debug=True)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    price = db.Column(db.Integer())

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return "Item {}".format(self.name)


@app.route('/')
def indexs():
    return "Neighborrow."


@app.route('/items/', methods=['GET', 'POST', 'DELETE'])
def items():
    if request.method == 'GET':
        items = Item.query.all()
        out = [
            {
                "pk": item.id,
                "name": item.name,
                "price": item.price
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


if __name__ == "__main__":
    app.run()
