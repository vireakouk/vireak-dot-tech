from flask import request, flash, render_template, redirect, url_for, session
from flask.views import View
from sqlalchemy.util.compat import u

from config import ADMIN_EMAILS
from app import db
from app.users.models import User
from app.users.forms import RegistrationForm, LoginForm
from app.utils.userutil import username_taken, email_taken, phone_invalid, phone_taken, format_phone
from app.utils.authutil import encrypt_password, credential_valid
from app.utils.dbutil import db_user

class Register(View):
    methods = ['GET', 'POST']
    def dispatch_request(self):
        form = RegistrationForm()

        if request.method == 'POST':
            if form.validate_on_submit():
                username = form.username.data.lower().strip()
                email = form.email.data.lower().strip()
                phone = form.phone.data.lower().strip()
                password = form.password.data
                
                try:
                    if username_taken(username):
                        flash(f'This username { username } is taken. Please use another username!', 'error')
                        return redirect(url_for(request.endpoint))

                    if email_taken(email):
                        flash(f'This email { email } is already registered. Please use another email!', 'error')
                        return redirect(url_for(request.endpoint))
                    
                    if phone_invalid(phone):
                        flash(f'This phone { phone } format is incorrect. Please re-enter correct phone format with leading +.', 'error')
                        return redirect(url_for(request.endpoint))

                    if phone_taken(phone):
                        flash(f'This phone { phone } is already registered. Please use another number!', 'error')
                        return redirect(url_for(request.endpoint))

                    phone = format_phone(phone)
                    password = encrypt_password(password)
                    is_admin = True if email in ADMIN_EMAILS else False
                    new_user = User(username=username, email=email, phone=phone, password=password, is_admin=is_admin)
                    db.session.add(new_user)
                    db.session.commit()
                    flash(f'Account { username } is successfully created! You can now login!', 'success')
                    return redirect(url_for('users.Login'))
                except Exception as e:
                    #for debugging purpose only
                    flash(f'Error: { e }', 'error')
                    return redirect(url_for(request.endpoint))

        return render_template('register.html', form=form)

class Login(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        form = LoginForm()
        if request.method == 'POST':
            username = form.username.data
            password = form.password.data

            # try:
            if credential_valid(username, password):
                current_user = db_user(username=username)
                session['active_user'] = {
                    'id': current_user.id,
                    'username': current_user.username,
                    'is_authenticated': True
                }

                return redirect(url_for('users.Dashboard'))
            # except:
            #     flash('Login Unsuccessful. Please check username and password again', 'error')
            #     return redirect(url_for(request.endpoint))

        return render_template('login.html', form=form)

class Dashboard(View):
    methods = ['GET']
    def dispatch_request(self):      
        return 'Hello World'

class Logout(View):
    methods = ['GET']
    def dispatch_request(self):      
        return 'Hello World'

class ResetPassword(View):
    methods = ['GET']
    def dispatch_request(self):      
        return 'Hello World'

class UpdateProfile(View):
    methods = ['GET']
    def dispatch_request(self):      
        return 'Hello World'

class DeleteAccount(View):
    methods = ['GET']
    def dispatch_request(self):      
        return 'Hello World'