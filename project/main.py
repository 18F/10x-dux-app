from flask import Blueprint, render_template
from . import db

main = Blueprint('main', __name__, static_folder='static', template_folder='template')

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
def profile():
    return render_template('profile.html')
