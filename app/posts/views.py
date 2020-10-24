from flask import render_template
from flask.views import View

class Blog(View):
    methods = ["GET"]
    def dispatch_request(self):      
        return "Hello World"

class SinglePost(View):
    methods = ["GET"]
    def dispatch_request(self):      
        return "Hello World"

class EditPost(View):
    methods = ["GET"]
    def dispatch_request(self):      
        return "Hello World"

class DeletePost(View):
    methods = ["GET"]
    def dispatch_request(self):      
        return "Hello World"