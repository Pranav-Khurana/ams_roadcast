import os
from flask import Blueprint, jsonify, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Roster, Attendance
from datetime import datetime
import base64

staff_bp = Blueprint('staff_routes', __name__, url_prefix='/staff')


@staff_bp.route('/portal')
@login_required
def portal():
    if current_user.role != 'Staff':
        flash('You are not authorized to view this page', 'error')
        return redirect(url_for('auth_routes.logout'))

    shifts = db.session.query(Roster, Attendance).outerjoin(
        Attendance,
        (Roster.id == Attendance.shift_id) & (Attendance.staff_id == current_user.id)
    ).filter(Roster.staff_id == current_user.id).all()

    return render_template('staff/staff_portal.html', shifts=shifts)


@staff_bp.route('/mark_attendance/<int:shift_id>')
@login_required
def mark_attendance(shift_id):
    if current_user.role != 'Staff':
        flash('You are not authorized to view this page', 'error')
        return redirect(url_for('auth_routes.logout'))

    existing_attendance = Attendance.query.filter_by(shift_id=shift_id, staff_id=current_user.id).first()
    if existing_attendance:
        flash('Attendance already marked for this shift', 'error')
        return redirect(url_for('staff_routes.portal'))

    return render_template('staff/mark_attendance.html', shift_id=shift_id)

@staff_bp.route('/submit_attendance', methods=['POST'])
@login_required
def submit_attendance():
    if current_user.role != 'Staff':
        return jsonify({'message': 'You are not authorized to mark attendance'}), 403

    image_data = request.form.get('image')
    shift_id = request.form.get('shift_id')

    if image_data and shift_id:
        try:
            # Decode base64 image data
            image_data = base64.b64decode(image_data.split(',')[1], validate=True)

            # Ensure directory exists
            image_dir = os.path.join(os.getcwd(), 'static', 'images')
            if not os.path.exists(image_dir):
                os.makedirs(image_dir)

            # Save image to a file
            image_path = os.path.join(image_dir, f"{current_user.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
            with open(image_path, 'wb') as f:
                f.write(image_data)

            # Example: Store attendance in database
            new_attendance = Attendance(staff_id=current_user.id, shift_id=shift_id, timestamp=datetime.now(), image_path=image_path)
            db.session.add(new_attendance)
            db.session.commit()

            flash('Attendance marked successfully', 'success')
        except Exception as e:
            flash(f'Error marking attendance: {str(e)}', 'error')

    else:
        flash('Missing image data or shift ID', 'error')

    return redirect(url_for('staff_routes.portal'))
