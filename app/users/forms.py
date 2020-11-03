from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, Length

class RegistrationForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired(), Length(min=2, max=24)])
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    phone = StringField(label="WhatsApp or Telegram Number (starting with +country code)", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    password_again = PasswordField(label="Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField(label="Sign Up")

class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Sign In")