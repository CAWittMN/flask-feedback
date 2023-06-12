from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User model"""

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship("Feedback", backref="user", cascade="all, delete")

    @classmethod
    def name_dict(cls, name):
        split_name = name.split()
        name_dict = {"first_name": split_name[0], "last_name": split_name[1]}
        return name_dict

    @classmethod
    def register(cls, username, password, email, name):
        """register a new user"""

        hashed_pswd = bcrypt.generate_password_hash(password)
        hashed_pswd_utf8 = hashed_pswd.decode("utf8")
        name_ = cls.name_dict(name)
        new_user = cls(
            username=username,
            password=hashed_pswd_utf8,
            email=email,
            first_name=name_["first_name"],
            last_name=name_["last_name"],
        )

        db.session.add(new_user)
        return new_user

    @classmethod
    def authenticate(cls, username, password):
        """authenticate a user account"""
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user

        return False


class Feedback(db.Model):
    """feedback model"""

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(
        db.String(20),
        db.ForeignKey("users.username"),
        nullable=False,
    )


def connect_db(app):
    db.init_app(app)
