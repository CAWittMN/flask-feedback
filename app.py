from flask import Flask, request, redirect, render_template, jsonify, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import User, Feedback, db, connect_db
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm
from werkzeug.exceptions import Unauthorized


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "feedbacksecretkey"
app.config["SQLALCHEMY_RECORD_QUERIES"] = True
# app.debug = True

# debug = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    """home page"""
    return redirect(url_for("register"))


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
        password = form.password.data

        new_user = User.register(username, password, email, name)

        db.session.commit()
        session["username"] = new_user.username

        return redirect(f"/users/{new_user.username}")

    return render_template("users/register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """login to a user account"""

    if "username" in session:
        return redirect(f'/users/{session["username"]}')

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect(f"/users/{user.username}")

        form.username.errors = ["Invalid username or password."]
    return render_template("/users/login.html", form=form)


@app.route("/logout")
def logout():
    """log out"""

    session.pop("username")
    return redirect(url_for("login"))


@app.route("/users/<username>")
def show_user(username):
    if "username" not in session or username != session["username"]:
        raise Unauthorized()

    user = User.query.get_or_404(username)
    form = DeleteForm()

    return render_template("users/show.html", user=user, form=form)


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    if "username" not in session or username != session["username"]:
        raise Unauthorized()

    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect(url_for("login"))


@app.route("/users/<username>/feedback/new", methods=["GET", "POST"])
def new_feedback(username):
    if "username" not in session or username != session["username"]:
        raise Unauthorized()

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )

        db.session.add(new_feedback)
        db.session.commit()

        return redirect(url_for("show_user", username=username))

    return render_template("feedback/new.html", form=form)


@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)

    if "username" not in session or feedback.username != session["username"]:
        raise Unauthorized()

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.add(feedback)
        db.session.commit()

        return redirect(url_for("show_user", username=feedback.username))

    return render_template("/feedback/edit.html", form=form, feedback=feedback)


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)

    if "username" not in session or feedback.username != session["username"]:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(url_for("show_user", username=feedback.username))
