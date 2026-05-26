from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from models import db, User, Patient, Doctor

auth_bp = Blueprint('auth', __name__)
bcrypt  = Bcrypt()


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']
        role     = request.form['role']
        name     = request.form['full_name']

        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('auth.register'))

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        user      = User(email=email, password_hash=hashed_pw, role=role)
        db.session.add(user)
        db.session.flush()

        if role == 'patient':
            patient = Patient(
                user_id   = user.id,
                full_name = name,
                age       = request.form.get('age'),
                gender    = request.form.get('gender'),
                phone     = request.form.get('phone')
            )
            db.session.add(patient)
        elif role == 'doctor':
            doctor = Doctor(
                user_id        = user.id,
                full_name      = name,
                specialization = request.form.get('specialization'),
                license_number = request.form.get('license_number')
            )
            db.session.add(doctor)

        db.session.commit()
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']
        user     = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            if user.role == 'patient':
                return redirect(url_for('patient.dashboard'))
            elif user.role == 'doctor':
                return redirect(url_for('doctor.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))