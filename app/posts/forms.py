from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField(label='Give your post a title (max 128 characters)', validators=[DataRequired(), Length(max=128)])
    content = TextAreaField(label='Content', validators=[DataRequired()])
    tag = StringField(label='Tag', validators=[Length(max=24)])
    submit = SubmitField(label='Post!')