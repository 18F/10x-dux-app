from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .queries import get_public_items, get_sensitve_items
from . import db

main = Blueprint('main', __name__, static_folder='static', template_folder='template')

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/public')
def public():
    return render_template('public.html', items=get_public_items())

@main.route('/sensitive')
@login_required
def sensitive():
    return render_template('sensitive.html', items=get_sensitve_items())

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
