from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Doctor, Patient, Scan, User

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'doctor':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))

    doctor      = Doctor.query.filter_by(user_id=current_user.id).first()
    total_scans = Scan.query.count()
    total_patients = Patient.query.count()
    recent_scans = Scan.query.order_by(Scan.created_at.desc()).limit(5).all()

    return render_template('doctor/dashboard.html',
        doctor         = doctor,
        total_scans    = total_scans,
        total_patients = total_patients,
        recent_scans   = recent_scans
    )


@doctor_bp.route('/patients')
@login_required
def patients():
    if current_user.role != 'doctor':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))

    all_patients = Patient.query.all()
    return render_template('doctor/patients.html', patients=all_patients)


@doctor_bp.route('/scan/<int:scan_id>')
@login_required
def scan_detail(scan_id):
    if current_user.role != 'doctor':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))

    scan    = Scan.query.get_or_404(scan_id)
    patient = Patient.query.get(scan.patient_id)

    return render_template('doctor/scan_detail.html', scan=scan, patient=patient)