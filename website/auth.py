from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            flash('Logged in succesfully!', category='success')
            login_user(user, remember=True)
            if user.is_admin:
                return redirect(url_for('admin.admin_panel')) # Redirect admin to the admin panel
            else:
                return redirect(url_for('views.home'))
        else:
            flash('Invalid credentials.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/admin-sign-up', methods=['GET', 'POST'])
def admin_sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exist.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(first_name) <2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be 7 characters long.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256', salt_length=16), is_admin=True)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Admin account created and logged in.', category='success')
            return redirect(url_for('admin.admin_panel'))
        
    return render_template("admin_sign_up.html", user=current_user)
    