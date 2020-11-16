from flask import jsonify
from flask.views import MethodView

from app.utils.dbutil import db_user

class Userapi(MethodView):

    def get(self, username:str):
        try:
            user = db_user(username=username)
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

        except:
            return jsonify({'error': 'user not found'}), 400
            