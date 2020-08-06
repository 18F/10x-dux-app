from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import environ
from .queries import get_user
from .commands import generate_public_items, generate_sensitive_items
from .persistence import db

def create_app_data(app, db):
    with app.app_context():
        db.create_all()

    if not generate_public_items(app.app_context()):
        raise RuntimeError('Data generation failed')

    if not generate_sensitive_items(app.app_context()):
        raise RuntimeError('Data generation failed')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = environ.get('SECRET_KEY', 'LOCALDEVONLY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    from . import models

    if environ.get('CREATE_DATA', False):
        create_app_data(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        print('User loaded!')
        return get_user(user_id)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import  main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
