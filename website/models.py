from . import db  # dot means same package
from flask_login import UserMixin
from sqlalchemy.sql import func


class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shop_name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(150), unique=True)
    contact = db.Column(db.String(13))
    address = db.Column(db.String(240))
    users = db.relationship('User')
    employees = db.relationship('Employee')
    join_requests = db.relationship('JoinRequest')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    contact = db.Column(db.String(13))
    password = db.Column(db.String(500))
    first_name = db.Column(db.String(25))
    last_name = db.Column(db.String(25))
    role = db.Column(db.String(5))
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(500))
    full_name = db.Column(db.String(100))
    contact = db.Column(db.String(13))
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))


class JoinRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))
    accept_date = db.Column(db.DateTime(timezone=True), default=func.now())
    accepted_by = db.Column(db.Integer, db.ForeignKey('user.id'))
