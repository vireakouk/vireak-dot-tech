from datetime import datetime

from app import db

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.SmallInterger, primary_key=True, autoincrement=True)
    author_id = db.Column(db.SmallInterger, ForeignKey=("users.id"), nullable=False)
    post_id = db.Column(db.SmallInterger, ForeignKey=("posts.id"), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    date_posted= db.Column(db.Datetime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Comment('{ self.comment.author }', '{ self.comment.parent_post }', '{ self.date_posted }')"