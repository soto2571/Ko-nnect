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

    # Loop to generate the next 2 weeks (14 days) of calendar dates
    for i in range(-6, 15):  # Adjust range as needed
        date = today + timedelta(days=i)
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

    return render_template(
        "home.html", 
        user=current_user, 
        dates=dates, 
        schedules=schedules, 
        today_schedule=today_schedule, 
        calendar_dates=calendar_dates
    )