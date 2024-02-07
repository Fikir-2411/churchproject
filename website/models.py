from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    age_range = db.Column(db.String(10))
    marital_status = db.Column(db.String(50))
    address = db.Column(db.String(200))
    phone_number = db.Column(db.String(40))
    email = db.Column(db.String(30), unique=True)
    former_church_name = db.Column(db.String(100))
    former_church_address = db.Column(db.String(100))
    prior_ministry = db.Column(db.String(100))
    current_ministry = db.Column(db.String(100))
    comments = db.Column(db.String(500))
    has_children = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    children = db.relationship('Child', backref='member', lazy=True)

class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    birthDate = db.Column(db.Date)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)