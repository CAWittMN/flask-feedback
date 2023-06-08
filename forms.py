from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email,


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    name = StringField("Name", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password")

    def validate_first_last_name()


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])
