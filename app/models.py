from datetime import datetime
import hashlib
from flask import request
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import db, app, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    fname=db.Column(db.String(20), nullable=False)
    lname=db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True ,nullable=False)
    password=db.Column(db.String(60), nullable=False)