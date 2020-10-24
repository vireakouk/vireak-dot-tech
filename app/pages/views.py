from flask import render_template
from flask.views import View

class Home(View):
    methods = ["GET"]
    def dispatch_request(self):      
        return render_template("index.html", is_homepage=True)
