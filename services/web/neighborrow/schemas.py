from .models import Item, Location, User
from . import ma

from marshmallow import fields, post_load


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'created', 'modified', 'email', 'phone', 'password')
        ordered = True

    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    phone_name = fields.Integer(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True, read_only=True)

    @post_load
    def create(self, data, **kwargs):
        if not data:
            return None
        password = data.pop('password')
        return User(**data, password=User.generate_hash(password))


class PublicUserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name')
        ordered = True


class ItemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'created', 'modified', 'owner', 'price', 'is_available')
        ordered = True

    owner = fields.Nested(PublicUserSchema)

    @post_load
    def create(self, data, **kwargs):
        if not data:
            return None
        return Item(**data)


class CoordsField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return {}
        return {'lon': value[0], 'lat': value[1]}


class LocationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'address', 'lon', 'lat', 'coords', 'distance')
        ordered = True

    address = fields.String(required=True)
    lon = fields.Float(required=True)
    lon = fields.Float(required=True)

    coords = CoordsField(write_only=True)
    distance = fields.Float(write_only=True)

    @post_load
    def create(self, data, **kwargs):
        if not data:
            return None
        return Location(**data)
