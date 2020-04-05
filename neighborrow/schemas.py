from . import ma
from marshmallow import fields


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'created', 'modified', 'phone')
        ordered = True


class PublicUserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name')
        ordered = True


class ItemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'created', 'modified', 'owner', 'price', 'is_available')
        ordered = True

    owner = fields.Nested(PublicUserSchema)


class LocationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'address', 'lon', 'lat', 'coords')
        ordered = True

    lon = fields.Float()
    lon = fields.Float()
