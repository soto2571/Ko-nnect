from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from .models import User, Schedule
from . import db
from werkzeug.security import generate_password_hash

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin.admin_panel'))
    
    user_schedules = Schedule.query.filter_by(employee_id=current_user.id).all()

    return render_template("home.html", user=current_user, schedules=user_schedules)
