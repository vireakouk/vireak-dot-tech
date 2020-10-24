from datetime import datetime

from app import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.SmallInterger, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    email = db.Column(db.String(128), unique=True, nullable=False)
    phone = db.Column(db.String(32), unique=True, nullable=False)
    is_admin = db.Column(db.Boolen, nullable=False, server_default=str(0))
    date_registered = db.Column(db.Datetime, nullable=False, default=datetime.utcnow)
    posts = db.relationship("Post", backref="author", lazy=True)
    comments = db.relationship("Comment", backref="author", lazy=True)

    def __repr__(self) -> str:
        return f"User('{ self.username }', '{ self.email }')"

