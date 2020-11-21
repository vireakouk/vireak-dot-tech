from app.api.views import SECRET_KEY
import jwt

from flask import jsonify, request
from flask.views import MethodView

from config import DevConfig
from app.utils.dbutil import db_user
from app.utils.authutil import token_decoded

SECRET_KEY = DevConfig.SECRET_KEY

class Userapi(MethodView):

    def get(self, username:str):

        user = db_user(username=username)
        if not user:
            return jsonify({'error': 'user not found'}), 400

        user_token = token_decoded()

        if user_token['status']=='missing':
            return jsonify({'message': 'a valid token is missing. Permission denied.'}), 401
        if user_token['status']=='expired':
            return jsonify({'message': 'token expired. Please obtain new token.'}), 401
        if user_token['status']=='invalid':
            return jsonify({'message': 'invalid token.'}), 401

        if user_token['status']=='valid':
            if user_token['username'] != username:
                return jsonify({'error': 'permission denied'}), 401

            api_response = []
            user_payload = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'phone': user.phone,
                'date_registered': user.date_registered
            }
            api_response.append(user_payload)

            return jsonify(api_response), 200

        return jsonify({'error': 'permission denied'}), 401
            