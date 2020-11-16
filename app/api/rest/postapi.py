from flask import request, jsonify
from flask.views import MethodView

from app.utils.dbutil import db_posts

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