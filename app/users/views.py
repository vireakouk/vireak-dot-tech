from flask import render_template
from flask.views import View

class Register(View):
    methods = ["GET"]
    def dispatch_request(self):      
        return "Hello World"

class Login(View):
    methods = ["GET"]
    def dispatch_request(self):      
        return "Hello World"

class Logout(View):
    methods = ["GET"]
    def dispatch_request(self):      
        return "Hello World"

class Dashboard(View):
    methods = ["GET"]
    def dispatch_request(self):      
        return "Hello World"
        
class ResetPassword(View):
    methods = ["GET"]
    def dispatch_request(self):      
        return "Hello World"

class UpdateProfile(View):
    methods = ["GET"]
    def dispatch_request(self):      
        return "Hello World"

class DeleteAccount(View):
    methods = ["GET"]
    def dispatch_request(self):      
        return "Hello World"