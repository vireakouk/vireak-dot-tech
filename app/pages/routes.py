from flask import Blueprint

from .views import Home

pages = Blueprint("pages", __name__)

pages.add_url_rule("/", view_func=Home.as_view("Home"))