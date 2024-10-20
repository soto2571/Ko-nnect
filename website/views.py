from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from .models import Schedule
from datetime import datetime, timedelta
import holidays  # Import the holidays library

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin.admin_panel'))

    today = datetime.now()
    today_date = today.strftime('%Y-%m-%d')
    dates = []
    schedules = {}
    today_schedule = None
    calendar_dates = []
    total_hours_worked = 0

    # Get Puerto Rico holidays for the current year
    pr_holidays = holidays.PR(years=today.year)

    # Loop for the next 14 days for the schedule cards
    for i in range(14):
        date = today + timedelta(days=i)
        formatted_date = date.strftime('%Y-%m-%d')
        schedules[formatted_date] = Schedule.query.filter(
            Schedule.employee_id == current_user.id,
            Schedule.shift_start >= date.replace(hour=0, minute=0, second=0, microsecond=0),
            Schedule.shift_end < date.replace(hour=23, minute=59, second=59, microsecond=999999)
        ).first()

        if formatted_date == today_date:
            today_schedule = schedules[formatted_date]

        dates.append(date)

    # Set the start date of the week (Sunday) for the calendar
    start_of_week = today - timedelta(days=today.weekday() + 1)

    # Loop to generate the next 2 weeks (14 days) of calendar dates from the fixed Sunday
    for i in range(21):  # Adjust the range to show the static calendar view
        date = start_of_week + timedelta(days=i)
        formatted_date = date.strftime('%Y-%m-%d')

        is_holiday = date in pr_holidays
        holiday_name = pr_holidays.get(date, '')
        has_shift = formatted_date in schedules and schedules[formatted_date] is not None

        # Append to the calendar dates with shift and holiday data
        calendar_dates.append({
            'date': date,
            'is_holiday': is_holiday,
            'holiday_name': holiday_name,
            'has_shift': has_shift
        })

        # Calculate total hours worked in the current week
        if has_shift:
            shift = schedules[formatted_date]
            worked_hours = (shift.shift_end - shift.shift_start).total_seconds() / 3600
            total_hours_worked += worked_hours

    # Deduct break time if hours worked exceed 5
    if total_hours_worked > 5:
        total_hours_worked -= 1  # Deduct 1 hour for the break

    return render_template(
        "home.html", 
        user=current_user, 
        dates=dates, 
        schedules=schedules, 
        today_schedule=today_schedule, 
        calendar_dates=calendar_dates,
        total_hours_worked=total_hours_worked  # Pass total hours worked to the template
    )