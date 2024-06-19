from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from models import db, User

auth_bp = Blueprint('auth_routes', __name__,)


@auth_bp.route('/')
def home():
    return render_template('auth/login.html')


@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        flash('Logged in successfully!', 'success')
        if user.role == 'Manager':
            return redirect(url_for('manager_routes.dashboard'))
        elif user.role == 'Staff':
            return redirect(url_for('staff_routes.portal'))
    else:
        flash('Login failed. Please check your credentials.', 'danger')
        return redirect(url_for('auth_routes.home'))


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('auth_routes.home'))


@auth_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'Manager':
        return redirect(url_for('manager_routes.dashboard'))
    elif current_user.role == 'Staff':
        return redirect(url_for('staff_routes.portal'))
    else:
        flash('Unknown user role', 'error')
        return redirect(url_for('auth_routes.logout'))
