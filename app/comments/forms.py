from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired

class CommentForm(FlaskForm):
    comment = TextAreaField(label='Leave a reply', validators=[DataRequired()])
    submit = SubmitField(label='Comment!')