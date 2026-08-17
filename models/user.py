from app import db


class User(db.Model):
    # id (int), username (text), password (text),
    id = db.Column(db.integer, primary_key=True)
    username = db.column(db.String(80), unique=True, nullable=False)
    password = db.column(db.String(80), nullable=False)
