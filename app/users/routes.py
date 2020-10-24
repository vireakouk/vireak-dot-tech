from flask import Blueprint

from .views import Register, Login, Logout, Dashboard, ResetPassword, UpdateProfile, DeleteAccount

users = Blueprint("users", __name__)

users.add_url_rule("/register", view_func=Register.as_view("Register"))
users.add_url_rule("/login", view_func=Login.as_view("Login"))
users.add_url_rule("/logout", view_func=Logout.as_view("Logout"))
users.add_url_rule("/<string:username>", view_func=Dashboard.as_view("Dashboard"))
users.add_url_rule("/<string:username>/resetpassword", view_func=ResetPassword.as_view("ResetPassword"))
users.add_url_rule("/<string:username>/updateprofile", view_func=UpdateProfile.as_view("UpdateProfile"))
users.add_url_rule("/<string:username>/deleteaccount", view_func=DeleteAccount.as_view("DeleteAccount"))

