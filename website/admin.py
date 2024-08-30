from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import User, Schedule
from . import db
from werkzeug.security import generate_password_hash
from datetime import datetime

admin = Blueprint('admin', __name__)

@admin.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_panel():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    employees = User.query.all()
    schedules = Schedule.query.all()

    return render_template('admin_panel.html', employees=employees, schedules=schedules, user=current_user)

@admin.route('/create-user', methods=['POST'])
@login_required
def create_user():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    
    email = request.form.get('email')
    first_name = request.form.get('first_name')
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    
    if not email or not first_name or not password or not password_confirm:
        flash("All fields are required!")
        return redirect(url_for('admin.admin_panel'))
    
    if password != password_confirm:
        flash("Passwords do not match!")
        return redirect(url_for('admin.admin_panel'))
    
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash("Email already in use!")
        return redirect(url_for('admin.admin_panel'))
    
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    new_user = User(email=email, first_name=first_name, password=hashed_password, is_admin=False)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        flash("User created successfully!")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {e}")
    
    return redirect(url_for('admin.admin_panel'))

@admin.route('/create-schedule', methods=['POST'])
@login_required
def create_schedule():
    if not current_user.is_admin:
        return redirect(url_for('home'))

    employee_id = request.form.get('employee_id')
    shift_start_str = request.form.get('shift_start')
    shift_end_str = request.form.get('shift_end')

    if not employee_id or not shift_start_str or not shift_end_str:
        flash('All fields are required to create a schedule.', category='error')
        return redirect(url_for('admin.admin_panel'))

    try:
        # Convert the string inputs to datetime objects
        shift_start = datetime.fromisoformat(shift_start_str)
        shift_end = datetime.fromisoformat(shift_end_str)

        new_schedule = Schedule(
            employee_id=employee_id, 
            shift_start=shift_start, 
            shift_end=shift_end, 
            created_by=current_user.id
        )
        
        db.session.add(new_schedule)
        db.session.commit()
        flash('Schedule has been created successfully', category='success')
    except ValueError as ve:
        flash(f"Invalid date format: {ve}", category='error')
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {e}", category='error')

    return redirect(url_for('admin.admin_panel'))