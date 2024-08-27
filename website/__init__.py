from flask import Flask, g, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, current_user
from dotenv import load_dotenv
import os
from flask_migrate import Migrate

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    db.init_app(app)
    migrate.init_app(app, db)

    from .admin import admin
    from .auth import auth
    from .views import views

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(auth, url_prefix='/auth')

    from .models import User, Schedule, VacationHours

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    @app.before_request
    def before_request():
        g.user = current_user

    # Ensure the database exists
    create_database(app)

    return app

def create_database(app):
    if not path.exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')