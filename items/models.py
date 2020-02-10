from flask import current_app as app

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


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
