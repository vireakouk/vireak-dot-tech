import bcrypt
from functools import wraps

from flask import redirect, url_for, session

from .dbutil import db_user

def encrypt_password(password):
    return bcrypt.hashpw(password.encode(encoding='UTF-8'), bcrypt.gensalt())

def credential_valid(username, password) -> bool:
    user_in_db = db_user(username=username)
    password_matched = bcrypt.checkpw(password.encode(encoding='UTF-8'), user_in_db.password)
    return True if user_in_db and password_matched else False

def login_required(func):
    @wraps(func)
    def f(*args, **kwargs):
        if not user_authenticated():
            return redirect(url_for('users.Login'))
        return func(*args, **kwargs)
    return f

def is_not_authenticated(func):
    @wraps(func)
    def f(*args, **kwargs):
        if user_authenticated():
            return redirect(url_for('users.Dashboard'))
        return func(*args, **kwargs)
    return f

def admin_required(func):
    @wraps(func)
    def f(*args, **kwargs):
        username = session['active_user']['username']
        if user_authenticated() and db_user(username=username).is_admin:
            return func(*args, **kwargs)
        return redirect(url_for('users.Dashboard'))
    return f

def user_authenticated() -> bool:
    return True if 'active_user' in session and session['active_user']['is_authenticated'] else False

