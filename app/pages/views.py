from app.utils.dbutil import db_posts
import textwrap

from flask import render_template
from flask.views import View

from app.utils.dbutil import db_posts

class Home(View):
    methods = ["GET"]
    
    def dispatch_request(self):
        f = textwrap
        posts = db_posts()      
        return render_template("index.html", posts=posts, textwrap=f, is_homepage=True)
