import bcrypt
from functools import wraps
import jwt

from flask import redirect, url_for, session, jsonify, request

from config import DevConfig
from .dbutil import db_user

SECRET_KEY = DevConfig.SECRET_KEY

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

# def token_required(func):
#     @wraps(func)
#     def f(*args, **kwargs):
#         auth_header = request.headers.get('Authorization')
#         user_token = auth_header.split(' ')[1] if auth_header else None

#         if not user_token:
#             return jsonify({'message': 'a valid token is missing. Permission denied.'}), 401

#         try:
#             user_token_decoded = jwt.decode(jwt=user_token, key=SECRET_KEY, algorithms='HS256')
#             user_id = user_token_decoded['sub']
#             user_in_db = db_user(id=user_id)

#             if user_in_db and user_in_db.username==user_token_decoded['name'] and user_in_db.email==user_token_decoded['email']:
#                 return func(*args, **kwargs)
#         except jwt.ExpiredSignatureError:
#             return jsonify({'message': 'Token expired. Please obtain new token.'}), 401
#         except:
#             return jsonify({'message': 'Invalid token.'}), 401
#     return f

# def token_required(func):
#     @wraps(func)
#     def f(*args, **kwargs):
#         if user_token()=='missing':
#             return jsonify({'message': 'a valid token is missing. Permission denied.'}), 401
#         if user_token()=='expired':
#             return jsonify({'message': 'Token expired. Please obtain new token.'}), 401
#         if user_token()=='invalid':
#             return jsonify({'message': 'Invalid token.'}), 401
#         if user_token()=='valid':
#             return func(*args, **kwargs)
#     return f

# def user_token() -> str:
#     auth_header = request.headers.get('Authorization')
#     user_token = auth_header.split(' ')[1] if auth_header else None

#     if not user_token:
#         return 'missing'
    
#     try:
#         user_token_decoded = jwt.decode(jwt=user_token, key=SECRET_KEY, algorithms='HS256')
#         user_id = user_token_decoded['sub']
#         user_in_db = db_user(id=user_id)

#         if user_in_db and user_in_db.username==user_token_decoded['name'] and user_in_db.email==user_token_decoded['email']:
#             return 'valid'
#     except jwt.ExpiredSignatureError:
#         return 'expired'
#     except:
#         return 'invalid'

def token_required(func):
    @wraps(func)
    def f(*args, **kwargs):
        user_token = token_decoded()
        if user_token['status']=='missing':
            return jsonify({'message': 'a valid token is missing. Permission denied.'}), 401
        if user_token['status']=='expired':
            return jsonify({'message': 'Token expired. Please obtain new token.'}), 401
        if user_token['status']=='invalid':
            return jsonify({'message': 'Invalid token.'}), 401
        if user_token['status']=='valid':
            return func(*args, **kwargs)
    return f

def token_decoded() -> dict:
    auth_header = request.headers.get('Authorization')
    user_token = auth_header.split(' ')[1] if auth_header else None

    token_decoded = {}

    if not user_token:
        token_decoded['status'] = 'missing' 
    
    try:
        user_token_decoded = jwt.decode(jwt=user_token, key=SECRET_KEY, algorithms='HS256')
        user_id = user_token_decoded['sub']
        user_in_db = db_user(id=user_id)

        if user_in_db and user_in_db.username==user_token_decoded['name'] and user_in_db.email==user_token_decoded['email']:
            token_decoded = {
                'status': 'valid',
                'username': user_in_db.username,
                'id': user_in_db.id
            } 
    except jwt.ExpiredSignatureError:
        token_decoded['status'] = 'expired'
    except:
        token_decoded['status'] = 'invalid'
    return token_decoded
