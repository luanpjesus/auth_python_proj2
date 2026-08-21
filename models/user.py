from flask_login import UserMixin

from database import db


class User(db.Model, UserMixin):
    # id (int), username (text), password (text),
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(80),
        nullable=False,
        unique=True,
    )
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
