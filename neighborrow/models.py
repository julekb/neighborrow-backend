from . import db


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    price = db.Column(db.Integer())

    # owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    # owner = db.relationship('User', backref=db.backref('items', lazy=True))

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return "Item {}".format(self.name)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())

    phone = db.Column(db.Integer)

    # items = db.relationship('Item', backref='user', lazy=True, nullable=True)


# class UserItemThrough(db.Model):
    # __tablename__ = 'useritemthrough'
    #
    # id = db.Column(db.Integer, primary_key=True)
