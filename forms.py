from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, ValidationError, Length


def check_name(form, field):
    if len(field.data.split()) != 2:
        raise ValidationError("Please provide only your first and last name.")


class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            Length(max=20, message="Username 20 characters maximum."),
            InputRequired(message="Please enter a username."),
        ],
    )
    name = StringField(
        "Name",
        validators=[
            Length(max=30, message="Name is too long"),
            InputRequired(message="Please enter a name."),
            check_name,
        ],
    )
    email = StringField(
        "Email",
        validators=[
            Length(max=30, message="Email is too long"),
            InputRequired(message="Please enter a email address."),
            Email(message="Not a valid email address."),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(message="Please enter a password."),
            Length(
                min=6, max=30, message="Password must be at least 6 characters long."
            ),
        ],
    )


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])
