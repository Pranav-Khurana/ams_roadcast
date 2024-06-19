from app import db
from flask_login import UserMixin
from datetime import datetime


# Define User Model
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(30), nullable=True)
    lname = db.Column(db.String(30), nullable=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


# Define Shift Model
class Roster(db.Model):
    __tablename__ = 'roster'
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    day_of_week = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    def __repr__(self):
        return f'<Shift {self.id}>'


# Define Attendance Model
class Attendance(db.Model):
    __tablename__ = 'attendances'
    id = db.Column(db.Integer, primary_key=True)
    shift_id = db.Column(db.Integer, db.ForeignKey('roster.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now, nullable=False)
    image_path = db.Column(db.String(255), nullable=False)  # Path to the captured image

    __table_args__ = (
        db.UniqueConstraint('staff_id', 'shift_id', name='uq_staff_shift'),
    )

    def __repr__(self):
        return f'<Attendance {self.id}>'
