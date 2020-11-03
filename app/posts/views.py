from flask import render_template, redirect, url_for, request, flash, session, abort
from flask.views import View

from app import db
from app.posts.forms import PostForm
from app.comments.forms import CommentForm
from app.comments.models import Comment
from app.utils.authutil import admin_required, login_required, user_authenticated
from app.utils.dbutil import db_posts, db_user, db_comments

class Blog(View):
    methods = ['GET']
    def dispatch_request(self):
        posts = db_posts()      
        return render_template('blog.html', posts=posts)

class SinglePost(View):
    methods = ['GET', 'POST']
    
    def dispatch_request(self, post_id:int):
        post = db_posts(id=post_id)
        comments = db_comments(post_id=post_id)
        user_loggedin = user_authenticated()

        form = CommentForm()
        if user_loggedin:
            if request.method == 'POST':
                if form.validate_on_submit():
                    comment = form.comment.data
                    try:
                        username = session['active_user']['username']
                        author = db_user(username=username)
                        parent_post = db_posts(id=post_id)
                        new_comment = Comment(comment=comment, parent_post=parent_post, author=author) 
                        db.session.add(new_comment)
                        db.session.commit()
                        flash('Your comment is successfully posted.', 'success')
                        return redirect(url_for(request.endpoint, post_id=post_id))
                    except:
                        flash('Some errors occurred.', 'error')
                        return redirect(url_for(request.endpoint, post_id=post_id))

        return render_template('post.html', post=post, comments=comments, form=form, user_loggedin=user_loggedin)

class EditPost(View):
    methods = ['GET', 'POST']

    @admin_required
    @login_required
    def dispatch_request(self, post_id:int):     
        username = session['active_user']['username']
        post = db_posts(id=post_id)

        if username != post.author.username:
            abort(403)

        form = PostForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                try:
                    post.title = form.title.data
                    post.content = form.content.data
                    post.tag = form.tag.data
                    db.session.commit()
                    flash('Your post is successfully updated.', 'success')
                    return redirect(url_for(request.endpoint, post_id=post_id))
                except Exception as e:
                    flash('Invalid update', 'error')
                    return redirect(url_for(request.endpoint, post_id=post_id))
        
        form.title.data = post.title
        form.content.data = post.content
        form.tag.data = post.tag
        return render_template('editpost.html', form=form)

class DeletePost(View):
    methods = ['GET', 'POST']
    
    @admin_required
    @login_required
    def dispatch_request(self, post_id:int):      
        username = session['active_user']['username']
        post = db_posts(id=post_id)
        
        if username != post.author.username:
            abort(403)
        
        for comment in post.comments:
            db.session.delete(comment)
        db.session.delete(post)
        db.session.commit()
        flash('Your post is successfully deleted.', 'success')
        return redirect(url_for('users.Dashboard'))