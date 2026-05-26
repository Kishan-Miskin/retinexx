from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Patient, Scan
import os
from werkzeug.utils import secure_filename
from utils import predict_class, allowed_file

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'patient':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))

    patient = Patient.query.filter_by(user_id=current_user.id).first()
    scans   = Scan.query.filter_by(patient_id=patient.id).order_by(Scan.created_at.desc()).all()
    return render_template('patient/dashboard.html', patient=patient, scans=scans)


@patient_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if current_user.role != 'patient':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        file = request.files.get('file')

        if not file or file.filename == '':
            flash('No file selected.', 'warning')
            return redirect(url_for('patient.upload'))

        if file and allowed_file(file.filename):
            filename  = secure_filename(file.filename)
            save_path = os.path.join('static/uploads', filename)
            file.save(save_path)

            diagnosis, probabilities = predict_class(save_path)

            patient = Patient.query.filter_by(user_id=current_user.id).first()
            scan = Scan(
                patient_id = patient.id,
                image_path = filename,
                prediction = diagnosis,
                confidence = max(probabilities) * 100
            )
            db.session.add(scan)
            db.session.commit()

            # Show result immediately like original app
            return render_template('patient/scan_result.html',
                diagnosis    = diagnosis,
                probabilities = probabilities,
                user_image   = filename,
                confidence   = round(max(probabilities) * 100, 2)
            )

        flash('Invalid file type.', 'danger')
        return redirect(url_for('patient.upload'))

    return render_template('patient/upload.html')


@patient_bp.route('/results')
@login_required
def results():
    if current_user.role != 'patient':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))

    patient = Patient.query.filter_by(user_id=current_user.id).first()
    scans   = Scan.query.filter_by(patient_id=patient.id).order_by(Scan.created_at.desc()).all()
    return render_template('patient/results.html', scans=scans, patient=patient)