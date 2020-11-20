import datetime

from flask import request, session, jsonify
from flask.views import MethodView, View
import jwt

from config import SECRET_KEY
from app.utils.dbutil import db_posts, db_user

class GetToken(View):
    methods = ['GET']

    def dispatch_request(self):
        username = session['active_user']['username']
        current_user = db_user(username=username)

        try:
            payload = {
                'iss': 'vireak.tech',
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
                'iat': datetime.datetime.ut(),
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

class Postapi(MethodView):

    def get(self, post_id:int):
        
        try:
            post = db_posts(id=post_id)
            api_response = []

            post_payload = {
                'id': post.id,
                'author': post.author.username,
                'title': post.title,
                'content': post.content,
                'date_posted': post.date_posted,
                'comments': []
            }
            for comment in post.comments:
                comment_payload = {
                    'author': comment.author.username,
                    'comment': comment.comment,
                    'date_posted': comment.date_posted
                }
                post_payload['comments'].append(comment_payload)
            api_response.append(post_payload)

            return jsonify(api_response), 200

        except:
            return jsonify({'error': 'post not found'}), 400

class Blogapi(MethodView):

    def get(self):
        # limit the number of post and starting ID with limit and offset arguments in the GET request
        # example: http:localhost:8000/api/rest/v1/blog?limit=10&offset=3
        try:
            limit = request.args.get("limit") if request.args.get("limit") else 5
            offset = request.args.get("offset") if request.args.get("offset") else 0
            limit = int(limit)
            offset = int(offset)
        except:
            return jsonify({'error': 'Invalid API query'}), 400

        posts = db_posts(limit=limit, offset=offset)
        api_response = []

        for post in posts:
            post_payload = {
                'id': post.id,
                'author': post.author.username,
                'title': post.title,
                'content': post.content,
                'date_posted': post.date_posted,
                'comments': []
            }
            for comment in post.comments:
                comment_payload = {
                    'author': comment.author.username,
                    'comment': comment.comment,
                    'date_posted': comment.date_posted
                }
                post_payload['comments'].append(comment_payload)
            api_response.append(post_payload)

        return jsonify(api_response), 200