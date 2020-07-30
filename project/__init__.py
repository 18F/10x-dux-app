from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = environ.get('SECRET_KEY', 'LOCALDEVONLY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db = SQLAlchemy()
    db.init_app(app)

    with app.app_context():
        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        from .main import  main as main_blueprint
        app.register_blueprint(main_blueprint)

        db.create_all()

        return app
