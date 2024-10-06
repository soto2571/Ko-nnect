from flask import Blueprint, render_template, request, redirect, url_for, abort, flash, jsonify
from flask_login import login_required, current_user
from .models import User, Schedule
from . import db
from werkzeug.security import generate_password_hash
from datetime import datetime, date, timedelta

admin = Blueprint('admin', __name__)

@admin.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_panel():
    if not current_user.is_admin:
        return redirect(url_for('home'))

    # Filter employees and schedules based on the current admin
    employees = User.query.filter_by(created_by=current_user.id).all()
    schedules = Schedule.query.filter_by(created_by=current_user.id).all()

    business_days_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Retrieve the admin's opening and closing times from current_user
    opening_time = current_user.opening_time
    closing_time = current_user.closing_time

    if opening_time and closing_time:
        # Combine opening and closing times with today's date to perform the time difference calculation
        from datetime import datetime

        today = datetime.now().date()
        opening_dt = datetime.combine(today, opening_time)
        closing_dt = datetime.combine(today, closing_time)

        # Calculate total business hours
        total_business_hours = (closing_dt - opening_dt).total_seconds() / 3600
    else:
        total_business_hours = 0  # Default if times are not set

    # Determine if schedules can be created (e.g., if total business hours exceed 9)
    can_create_schedule = total_business_hours <= 9

    # Filter schedules based on total working hours (8 hours work + 1 hour break)
    valid_schedules = []
    for schedule in schedules:
        total_hours = (schedule.shift_end - schedule.shift_start).total_seconds() / 3600 - 1  # Subtracting break time
        if total_hours >= 8:  # Only include valid schedules
            valid_schedules.append(schedule)

    return render_template(
        'admin_panel.html',
        employees=employees,
        schedules=valid_schedules,
        user=current_user,
        business_days_list=business_days_list,
        can_create_schedule=can_create_schedule
    )

@admin.route('/create-user', methods=['POST'])
@login_required
def create_user():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    
    email = request.form.get('email')
    first_name = request.form.get('first_name')
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    availability = request.form.get('availability')
    
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
    new_user = User(email=email, first_name=first_name, password=hashed_password, is_admin=False, availability=availability, created_by=current_user.id)
    
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

@admin.route('/delete_schedule/<int:id>', methods=["POST"])
@login_required
def delete_schedule(id):
    if not current_user.is_admin:
        return redirect(url_for('home'))
    
    schedule = Schedule.query.get_or_404(id) # ???
    try:
        db.session.delete(schedule) 
        db.session.commit()
        flash("Schedule deleted succesfully!", category='success')
    except Exception as e:
        db.session.rollback() # ???
        flash(f"An error ocurred while deleting the schedule: {e}", category='error')

    return redirect(url_for('admin.admin_panel'))

@admin.route('/delete_employee/<int:id>', methods=["POST"])
@login_required
def delete_employee(id):
    if not current_user.is_admin:
        return redirect(url_for('home'))
    
    employee = User.query.get_or_404(id) # ???
    try:
        db.session.delete(employee)
        db.session.commit()
        flash("Employee deleted succesfully!", category='success')
    except Exception as e:
        db.session.rollback() # ???
        flash(f"An error occurred while deleting the employee: {e}", category='error')
   
    return redirect(url_for('admin.admin_panel'))

@admin.route('/set-business-hours', methods=['POST'])
@login_required
def set_business_hours():
    if not current_user.is_admin:
        return redirect(url_for('home'))

    opening_time_str = request.form.get('opening_time')
    closing_time_str = request.form.get('closing_time')
    business_days = request.form.getlist('business_days')  # Get selected days

    try:
        # Save opening and closing time
        current_user.opening_time = datetime.strptime(opening_time_str, "%H:%M").time()
        current_user.closing_time = datetime.strptime(closing_time_str, "%H:%M").time()

        # Save business days as a comma-separated string
        current_user.business_days = ",".join(business_days)

        db.session.commit()
        flash("Business hours and days updated successfully!", category='success')
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {e}", category='error')

    return redirect(url_for('admin.admin_panel'))


def generate_schedule_for_employee(employee, duration, admin):
    start_hour = admin.opening_time
    end_hour = admin.closing_time
    business_days = list(map(int, admin.business_days.split(',')))  # Convert string to list of integers

    total_working_hours = (datetime.combine(date.today(), end_hour) - datetime.combine(date.today(), start_hour)).seconds / 3600 - 1 # substract 1 hour for break

    # Check if total working hours exceed 9
    if total_working_hours > 8:
        return # Do not generate the schedule if working hours exceed limit
    
    # Generate shifts for the given duration (in weeks)
    for day_offset in range(duration * 7):
        current_day = (date.today() + timedelta(days=day_offset)).weekday()

        # Only create shifts on business days
        if current_day in business_days:
            shift_start = datetime.combine(date.today() + timedelta(days=day_offset), start_hour)
            shift_end = datetime.combine(date.today() + timedelta(days=day_offset), end_hour)

            # Create the schedule for the employee
            new_schedule = Schedule(
                employee_id=employee.id,
                shift_start=shift_start,
                shift_end=shift_end,
                created_by=admin.id
            )
            db.session.add(new_schedule)

    db.session.commit()

@admin.route('/generate-schedule/<int:employee_id>/<int:duration>', methods=['POST'])
@login_required
def generate_schedule(employee_id, duration):
    if not current_user.is_admin:
        return redirect(url_for('home'))

    employee = User.query.get_or_404(employee_id)
    if not employee:
        flash("Employee not found!", category='error')
        return redirect(url_for('admin.admin_panel'))

    try:
        generate_schedule_for_employee(employee, duration, current_user)
        flash(f"Schedule for {employee.first_name} generated successfully!", category='success')
    except Exception as e:
        flash(f"An error occurred while generating the schedule: {e}", category='error')

    return redirect(url_for('admin.admin_panel'))

from flask import jsonify

@admin.route('/edit_schedule/<int:id>', methods=['POST'])
@login_required
def edit_schedule(id):
    if not current_user.is_admin:
        return redirect(url_for('home'))

    schedule = Schedule.query.get(id)
    if not schedule:
        return jsonify({'success': False, 'error': 'Schedule not found!'}), 404

    # Get updated values from the JSON request
    data = request.get_json()
    shift_start_str = data.get('shift_start')
    shift_end_str = data.get('shift_end')

    if not shift_start_str or not shift_end_str:
        return jsonify({'success': False, 'error': 'All fields are required to update the schedule.'}), 400

    try:
        # Convert the string inputs to datetime objects
        shift_start = datetime.fromisoformat(shift_start_str)
        shift_end = datetime.fromisoformat(shift_end_str)

        if shift_start >= shift_end:
            return jsonify({'success': False, 'error': 'Shift start time must be before the shift end time.'}), 400

        # Update the schedule
        schedule.shift_start = shift_start
        schedule.shift_end = shift_end
        db.session.commit()
        return jsonify({'success': True})
    except ValueError as ve:
        return jsonify({'success': False, 'error': f"Invalid date format: {ve}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f"An error occurred: {e}"}), 500