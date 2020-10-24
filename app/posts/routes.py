from flask import Blueprint

from .views import Blog, SinglePost, EditPost, DeletePost

posts = Blueprint("posts", __name__)

posts.add_url_rule("/blog", view_func=Blog.as_view("Blog"))
posts.add_url_rule("/post/<int:post_id>", view_func=SinglePost.as_view("SinglePost"))
posts.add_url_rule("/post/<int:post_id>/edit", view_func=EditPost.as_view("EditPost"))
posts.add_url_rule("/post/<int:post_id>/delete", view_func=DeletePost.as_view("DeletePost"))
