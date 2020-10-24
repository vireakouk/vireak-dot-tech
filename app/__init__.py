from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.users.routes import users
from app.posts.routes import posts
from app.pages.routes import pages

app = Flask(__name__)
app.config.from_object('config.DevConfig')

db = SQLAlchemy(app)
migrate = Migrate(app=app, db=db)

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(pages)
