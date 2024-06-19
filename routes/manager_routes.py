from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, User, Roster, Attendance
from werkzeug.security import generate_password_hash

manager_bp = Blueprint('manager_routes', __name__, url_prefix='/manager')


@manager_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'Manager':
        flash('You are not authorized to view this page', 'error')
        return redirect(url_for('auth_routes.logout'))
    staff_members = User.query.filter_by(role='Staff')
    return render_template('manager/manager_dashboard.html', staff_members=staff_members)


@manager_bp.route('/add_staff', methods=['GET', 'POST'])
@login_required
def add_staff():
    if current_user.role != 'Manager':
        flash('You are not authorized to view this page', 'error')
        return redirect(url_for('auth_routes.logout'))

    if request.method == 'POST':
        username = request.form.get('username')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password = request.form.get('password')
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
            return redirect(url_for('manager_routes.add_staff'))
        
        new_user = User(username=username, fname=firstname, lname=lastname, password=generate_password_hash(password), role='Staff')
        db.session.add(new_user)
        db.session.commit()

        flash('New staff member added successfully', 'success')
        print(url_for('manager_routes.dashboard'))
        return redirect(url_for('manager_routes.dashboard'))

    return render_template('manager/add_staff.html')


@manager_bp.route('/view_roster', methods=['GET'])
@login_required
def view_roster():
    if current_user.role != 'Manager':
        flash('You are not authorized to view this page', 'error')
        return redirect(url_for('auth_routes.logout'))

    roster = db.session.query(Roster, User.username).outerjoin(User, Roster.staff_id == User.id).all()
    return render_template('manager/view_roster.html', roster=roster)


@manager_bp.route('/view_attendance', methods=['GET'])
@login_required
def view_attendance():
    if current_user.role != 'Manager':
        flash('You are not authorized to view this page', 'error')
        return redirect(url_for('auth_routes.logout'))
    
    attendance_records = db.session.query(Attendance.timestamp, Attendance.image_path,
                                          User.username,
                                          Roster.start_time,
                                          Roster.day_of_week
                                          ).join(
                                              User, Attendance.staff_id == User.id
                                              ).join(
                                                  Roster, Attendance.shift_id == Roster.id
                                                  ).all()
    
    return render_template('manager/view_attendance.html', attendance_records=attendance_records)


@manager_bp.route('/assign_shift', methods=['GET', 'POST'])
@login_required
def assign_shift():
    if current_user.role != 'Manager':
        flash('You are not authorized to view this page', 'error')
        return redirect(url_for('auth_routes.logout'))

    if request.method == 'POST':
        staff_id = request.form.get('staff_id')
        day_of_week = request.form.get('day_of_week')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')

        new_shift = Roster(staff_id=staff_id, day_of_week=day_of_week, start_time=start_time, end_time=end_time)
        db.session.add(new_shift)
        db.session.commit()

        flash('New shift added to roster successfully', 'success')
        return redirect(url_for('manager_routes.view_roster'))

    staff_members = User.query.filter_by(role='Staff').all()
    return render_template('manager/add_shift.html', staff_members=staff_members)


@manager_bp.route('/edit_shift/<int:shift_id>', methods=['GET', 'POST'])
@login_required
def edit_shift(shift_id):
    if current_user.role != 'Manager':
        flash('You are not authorized to view this page', 'error')
        return redirect(url_for('auth_routes.logout'))

    shift = Roster.query.get_or_404(shift_id)

    if request.method == 'POST':
        shift.staff_id = request.form.get('staff_id')
        shift.day_of_week = request.form.get('day_of_week')
        shift.start_time = request.form.get('start_time')
        shift.end_time = request.form.get('end_time')

        db.session.commit()

        flash('Shift updated successfully', 'success')
        return redirect(url_for('manager_routes.view_roster'))

    staff_members = User.query.filter_by(role='Staff').all()
    return render_template('manager/edit_shift.html', shift=shift, staff_members=staff_members)
