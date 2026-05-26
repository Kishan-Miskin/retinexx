from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id            = db.Column(db.Integer, primary_key=True)
    email         = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role          = db.Column(db.String(20), nullable=False)  # 'patient' or 'doctor'
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship('Patient', backref='user', uselist=False)
    doctor  = db.relationship('Doctor',  backref='user', uselist=False)


class Patient(db.Model):
    __tablename__ = 'patients'
    id        = db.Column(db.Integer, primary_key=True)
    user_id   = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    age       = db.Column(db.Integer)
    gender    = db.Column(db.String(10))
    phone     = db.Column(db.String(20))

    scans = db.relationship('Scan', backref='patient', lazy=True)


class Doctor(db.Model):
    __tablename__ = 'doctors'
    id              = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    full_name       = db.Column(db.String(100), nullable=False)
    specialization  = db.Column(db.String(100))
    license_number  = db.Column(db.String(50))


class Scan(db.Model):
    __tablename__ = 'scans'
    id          = db.Column(db.Integer, primary_key=True)
    patient_id  = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    image_path  = db.Column(db.String(255), nullable=False)
    prediction  = db.Column(db.String(100))
    confidence  = db.Column(db.Float)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)