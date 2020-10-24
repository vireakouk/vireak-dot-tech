from datetime import datetime

from app import db

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.SmallInterger, primary_key=True, autoincrement=True)
    author_id = db.Column(db.SmallInterger, ForeignKey=("users.id"), nullable=False)
    title = db.Column(db.String(128), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted= db.Column(db.Datetime, nullable=False, default=datetime.utcnow)
    comments = db.relationship("Comment", backref="parent_post", lazy=True)

    def __repr__(self) -> str:
        return f"Post('{ self.post.author }', '{ self.title }', '{ self.date_posted }')"