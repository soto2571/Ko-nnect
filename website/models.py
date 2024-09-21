from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    is_admin = db.Column(db.Boolean, default=False)

    opening_time = db.Column(db.Time, nullable=True)
    closing_time = db.Column(db.Time, nullable=True)
    business_days = db.Column(db.String(20), nullable=True)

    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    availability = db.Column(db.String(500))

    schedules = db.relationship('Schedule', foreign_keys='Schedule.employee_id', backref='employee', cascade='all, delete-orphan')
    created_schedules = db.relationship('Schedule', foreign_keys='Schedule.created_by', backref='creator', cascade='all, delete-orphan')
    vacation_hours = db.relationship('VacationHours', foreign_keys='VacationHours.employee_id', backref='employee', cascade='all, delete-orphan')
    created_vacation_hours = db.relationship('VacationHours', foreign_keys='VacationHours.created_by', backref='creator', cascade='all, delete-orphan')

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Employee associated with the schedule
    shift_start = db.Column(db.DateTime)
    shift_end = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id')) # User who created the schedule

class VacationHours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Employee associated with the vacation hours
    hours_available = db.Column(db.Integer)
    hours_taken = db.Column(db.Integer)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id')) # User who created the vacation hours record