from flask import current_app as app
from flask import request

from . import db
from .models import User


@app.route('/login', methods=['post'])
def login():
        return


@app.route('/signup', methods=['post'])
def signup():
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    email = request.json.get('email')
    password = request.json.get('password')
    phone = request.json.get('password')

    if not (first_name or last_name or password or phone or email):
        raise
    # if User.query.filter(or_(email=email, phone=phone)):
    #     raise

    user = User(first_name=first_name, last_name=last_name, email=email, phone=phone)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
