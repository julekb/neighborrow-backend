import datetime as dt

from . import db
from .core import NModel, TimestampMixin

from flask_login import UserMixin
from geoalchemy2 import Geometry, func
from geoalchemy2.elements import WKTElement
from geoalchemy2.shape import to_shape
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

    def __repr__(self, *args, **kwargs):
        return f'User {self.id}: {self.first_name} {self.last_name}'

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class Location(NModel):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    geom = db.Column(Geometry(geometry_type='POINT'))
    address = db.Column(db.String(1024))

    def __init__(self, lon, lat, *args, **kwargs):
        geom = WKTElement('POINT(%s %s)' % (lon, lat))
        kwargs['geom'] = geom

        return super(Location, self).__init__(*args, **kwargs)

    @property
    def coords(self):
        if self.geom is not None:
            point = to_shape(self.geom)
            return [point.x, point.y]

    @classmethod
    def get_in_range(cls, lon, lat):
        def process(qs):
            for obj, distance in qs:
                obj.distance = distance
                yield obj
        point = WKTElement('POINT(%s %s)' % (lon, lat))
        qs = db.session.query(Location, func.ST_Distance_Shpere(Location.geom, point).label('distance')).order_by('distance')
        return process(qs)


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

    def __repr__(self):
        return f"Item {self.name}"

    @property
    def is_available(self):
        return True


class Rental(NModel):
    __tablename__ = 'rentals'

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, default=dt.datetime.utcnow())
    end_date = db.Column(db.DateTime, default=dt.datetime.utcnow())

    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'))
