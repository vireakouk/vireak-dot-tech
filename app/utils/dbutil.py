from app import db
from app.users.models import User
from app.posts.models import Post
from app.comments.models import Comment

def db_user(id=None, username=None, email=None, phone=None) -> object:
    if id:
        return db.session.query(User).filter(User.id==id).first()
    if username:
        return db.session.query(User).filter(User.username==username).first()
    if email:
        return db.session.query(User).filter(User.email==email).first()
    return db.session.query(User).filter(User.phone==phone).first()

def db_posts(id=None, author_id=None, author=None, limit=None, offset=None) -> object:
    if id:
        return db.session.query(Post).filter(Post.id==id).first()
    if author_id:
        return db.session.query(Post).filter(Post.author_id==author_id).all()
    if author:
        return db.session.query(Post).filter(Post.author==author).order_by(Post.id.desc()).all()
    if limit is not None and offset is not None:
       return db.session.query(Post).order_by(Post.id.desc()).limit(limit).offset(offset).all()
    
    return db.session.query(Post).order_by(Post.id.desc()).all()

def db_comments(id=None, post_id=None, thread_id=None, author=None, author_id=None, parent_post=None) -> object:
    if id:
        return db.session.query(Comment).filter(Comment.id==id).first()
    if post_id:
        return db.session.query(Comment).filter(Comment.post_id==post_id).all()
    if thread_id:
        return db.session.query(Comment).filter(Comment.thread_id==thread_id).all()
    if author:
        return db.session.query(Comment).filter(Comment.author==author).all()
    if author_id:
        return db.session.query(Comment).filter(Comment.author_id==author_id).all()
    if parent_post:
        return db.session.query(Comment).filter(Comment.parent_post==parent_post).all()
    return db.session.query(Comment).order_by(Comment.id.desc()).all()
