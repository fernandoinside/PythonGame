from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from functools import wraps
from config import mongo

auth_bp = Blueprint('auth', __name__)

# Dummy user data
users = {
    "fernando": "123456"
}

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('auth.login'))
    return wrap

@auth_bp.route('/')
@login_required
def home():
    targets = mongo.db.targets.find()
    return render_template('dashboard.html', targets=targets)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('auth.home'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

@auth_bp.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('auth.login'))
