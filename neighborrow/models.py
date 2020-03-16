import datetime as dt

from . import db

from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """
    From UserMixin:
    - is_authenticated
    - is_active
    - is_anonymous
    - get_id
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    password = db.Column(db.String(200),
                         primary_key=False,
                         unique=False,
                         nullable=False)

    phone = db.Column(db.Integer)

    items = relationship('Item', back_populates='owner')
    rented = relationship('Item', secondary='rentals')

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    price = db.Column(db.Integer())
    added_date = db.Column(db.DateTime, default=dt.datetime.utcnow())

    rentals = relationship('User', secondary='rentals')
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner = relationship('User', back_populates='items')

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return "Item {}".format(self.name)


class Rental(db.Model):
    __tablename__ = 'rentals'

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, default=dt.datetime.utcnow())
    end_date = db.Column(db.DateTime, default=dt.datetime.utcnow())

    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'))
