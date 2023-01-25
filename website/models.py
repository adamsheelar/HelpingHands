from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    zip_code = db.Column(db.String(150))
    search_post = db.Column(db.String(150))
    notes = db.relationship('Note')
    interest_1 = db.Column(db.String(150))
    interest_2 = db.Column(db.String(150))
    interest_3 = db.Column(db.String(150))
    interest_4 = db.Column(db.String(150))
    interest_5 = db.Column(db.String(150))
    points = db.Column(db.String(150))
    status = db.Column(db.String(150))


