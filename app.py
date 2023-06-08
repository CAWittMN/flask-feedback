from flask import Flask, request, redirect, render_template, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from models import User, db, connect_db
from forms import RegisterForm, LoginForm
from wtforms.validators import ValidationError


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "feedbacksecretkey"
app.config["SQLALCHEMY_RECORD_QUERIES"] = True
app.debug = True

debug = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    """home page"""
    return render_template("base.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """show register form and create a new user account"""
    if "current_user" in session:
        return redirect(f'users/{session["current_user"]}')

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        name = form.name.data
        if len(name.split()) > 2:
            ValidationError(message="Please enter first and last name only.")
