from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate




app = Flask(__name__)
app.config.from_object('config.DevConfig')

db = SQLAlchemy(app)
migrate = Migrate(app=app, db=db)

from app.users.routes import users
from app.posts.routes import posts
from app.pages.routes import pages

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(pages)

from app.users.models import User
from app.posts.models import Post
from app.comments.models import Comment