from flask import Blueprint

from app.api.views import GetToken
from .rest.userapi import Userapi
from .rest.postapi import Postapi, Blogapi 

api = Blueprint("api", __name__)

api.add_url_rule("/api/gettoken", view_func=GetToken.as_view("GetToken"))
api.add_url_rule("/api/rest/v1/user/<string:username>", view_func=Userapi.as_view("Userapi"))
api.add_url_rule("/api/rest/v1/post/<int:post_id>", view_func=Postapi.as_view("Postapi"))
api.add_url_rule("/api/rest/v1/blog", view_func=Blogapi.as_view("Blogapi"))