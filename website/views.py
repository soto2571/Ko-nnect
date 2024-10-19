from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from .models import User, Schedule
from . import db
from werkzeug.security import generate_password_hash
from datetime import datetime, date, timedelta

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin.admin_panel'))
    
    today = datetime.now()
    today_date = today.strftime('%Y-%m-%d')  # Format today's date
    dates = []
    schedules = {}
    today_schedule = None  # Initialize today_schedule

    # Calculate today and next 13 days
    for i in range(14):
        date = today + timedelta(days=i)
        formatted_date = date.strftime('%Y-%m-%d')  # Use this format for querying
        schedules[formatted_date] = Schedule.query.filter(
            Schedule.employee_id == current_user.id,
            Schedule.shift_start >= date.replace(hour=0, minute=0, second=0, microsecond=0),
            Schedule.shift_end < date.replace(hour=23, minute=59, second=59, microsecond=999999)
        ).first()  # Get the first schedule for that day if it exists
        
        # Check if the current date is today
        if formatted_date == today_date:
            today_schedule = schedules[formatted_date]  # Set today_schedule for today

        dates.append(date)

    return render_template("home.html", user=current_user, dates=dates, schedules=schedules, today_schedule=today_schedule)