from flask import request, flash, render_template, redirect, url_for, session, abort
from flask.views import View

from config import ADMIN_EMAILS
from app import db
from app.users.models import User
from app.posts.models import Post
from app.users.forms import RegistrationForm, LoginForm
from app.posts.forms import PostForm
from app.utils.userutil import username_taken, email_taken, phone_invalid, phone_taken, format_phone
from app.utils.authutil import encrypt_password, credential_valid, is_not_authenticated, login_required, admin_required, user_authenticated
from app.utils.dbutil import db_comments, db_posts, db_user

class Register(View):
    methods = ['GET', 'POST']

    @is_not_authenticated
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

        if user_authenticated():
            return redirect(url_for('users.Dashboard'))

        form = LoginForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                username = form.username.data
                password = form.password.data

                try:
                    if credential_valid(username, password):
                        current_user = db_user(username=username)
                        session['active_user'] = {
                            'id': current_user.id,
                            'username': current_user.username,
                            'is_authenticated': True
                        }
                        
                        return redirect(url_for('users.Dashboard'))
                    else:
                        flash(f'Login Unsuccessful. Please check username and password again.', 'error')
                        return redirect(url_for(request.endpoint))

                except Exception as e:
                    flash('Login Unsuccessful. Please check username and password again.', 'error')
                    return redirect(url_for(request.endpoint))

        return render_template('login.html', form=form)

class Dashboard(View):
    methods = ['GET']

    @login_required
    def dispatch_request(self):
        username = session['active_user']['username']
        current_user = db_user(username=username)
        if current_user.is_admin:
             return redirect(url_for('users.Admin'))

        return render_template('dashboard.html', username=username)

class Admin(View):
    methods = ['GET', 'POST']

    @login_required
    @admin_required
    def dispatch_request(self):
        form = PostForm()
        username = session['active_user']['username']
        author = db_user(username=username)
        posts = db_posts(author=author)

        if request.method == 'POST':
            if form.validate_on_submit():
                title = form.title.data
                content = form.content.data
                tag = form.tag.data

                try:
                    new_post = Post(author=author, title=title, content=content, tag=tag)
                    db.session.add(new_post)
                    db.session.commit()
                    flash('Your post is successfully submitted', 'success')
                    return redirect(url_for(request.endpoint))
                except Exception as e:
                    flash('Invalid inputs.', 'error')
                    return redirect(url_for(request.endpoint))

        return render_template('admin.html', username=username, form=form, posts=posts)

class Logout(View):
    methods = ['GET']
    
    @login_required
    def dispatch_request(self):
        session.clear()      
        return redirect(url_for('users.Login'))

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
    
    @login_required
    def dispatch_request(self, username:str):      
        current_username = session['active_user']['username']
        current_user = db_user(username=current_username)
        user_account = db_user(username=username)

        if not user_account:
            abort(403)

        #getting back to this later. This will delete everything. Need better functions to maintain content even users are deleted.
        if current_user.username == user_account.username or current_user.is_admin:
            user_comments = db_comments(author=user_account)
            user_posts = db_posts(author=user_account)
            for comment in user_comments:
                db.session.delete(comment)
            for post in user_posts:
                db.session.delete(post)
            db.session.delete(user_account)
            db.session.commit()

        if current_user.is_admin:
            flash(f'Account { username } is successfully deleted.', 'success')
            return redirect(url_for('users.Dashboard'))

        session.clear()
        flash(f'Account { username } is successfully deleted.', 'success')
        return redirect(url_for('users.Login'))