import datetime

import jwt
from flask import session, jsonify
from flask.views import View

from config import DevConfig
from app.utils.authutil import login_required
from app.utils.dbutil import db_user

SECRET_KEY = DevConfig.SECRET_KEY

class GetToken(View):
    methods = ['GET']

    @login_required
    def dispatch_request(self):
        username = session['active_user']['username']
        current_user = db_user(username=username)

        try:
            payload = {
                'iss': 'vireak.tech',
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
                'iat': datetime.datetime.utcnow(),
                'name': current_user.username,
                'email': current_user.email,
                'sub': current_user.id
            }
            token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm='HS256')
            token = token.decode('UTF-8')
            message = {
                'status': 'success',
                'token': token
            }
        except Exception as e:
            message = {
                'status': 'fail',
                'message': 'Unable to generate token. Please try again.'
            }
            return jsonify(message), 401

        return jsonify(message), 200
