from datetime import datetime
from sqlalchemy.orm import relationship

from app import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(24), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    phone = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, server_default=str(0))
    date_registered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    posts = db.relationship('app.posts.models.Post', backref='author', lazy=True)
    comments = db.relationship('app.comments.models.Comment', backref='author', lazy=True)

    def __repr__(self) -> str:
        return f"User('{ self.username }', '{ self.email }')"




