from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    is_admin = db.Column(db.Boolean, default=False)


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    shift_start = db.Column(db.DateTime)
    shift_end = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

class VacationHours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    hours_available = db.Column(db.Integer)
    hours_taken = db.Column(db.Integer)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))