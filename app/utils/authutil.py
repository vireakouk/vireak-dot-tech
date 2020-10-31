import bcrypt

from .dbutil import db_user

def encrypt_password(password):
    return bcrypt.hashpw(password.encode(encoding='UTF-8'), bcrypt.gensalt())

def credential_valid(username, password) -> bool:
    user_in_db = db_user(username=username)
    password_matched = bcrypt.checkpw(password.encode(encoding='UTF-8'), user_in_db.password)
    return True if user_in_db and password_matched else False

