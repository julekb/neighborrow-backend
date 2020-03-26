import datetime as dt

from . import db
from .core import NModel, TimestampMixin

from flask_login import UserMixin
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy.orm import relationship


class RevokedToken(NModel):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(200))

    @classmethod
    def is_jti_blacklisted(cls, jti):
        return bool(cls.query.filter_by(jti=jti).scalar is None)


class User(NModel,
           UserMixin,
           TimestampMixin):
    """
    From UserMixin:
    - is_authenticated
    - is_active
    - is_anonymous
    - get_id
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(200),
                         primary_key=False,
                         unique=False,
                         nullable=False)

    email = db.Column(db.String(64), unique=True, nullable=False)
    phone = db.Column(db.Integer)

    items = relationship('Item', back_populates='owner')
    rented = relationship('Item', secondary='rentals')

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class Location(NModel):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    addres = db.Column(db.String(1024))


class Item(NModel, TimestampMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.String(1024))
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


class Rental(NModel):
    __tablename__ = 'rentals'

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, default=dt.datetime.utcnow())
    end_date = db.Column(db.DateTime, default=dt.datetime.utcnow())

    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'))
