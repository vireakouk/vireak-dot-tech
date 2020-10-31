from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey 

from app import db

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(128), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    tag = db.Column(db.String)
    date_posted= db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comments = db.relationship('app.comments.models.Comment', backref='parent_post', lazy=True)

    def __repr__(self) -> str:
        return f"Post('{ self.post.author }', '{ self.title }', '{ self.date_posted }')"