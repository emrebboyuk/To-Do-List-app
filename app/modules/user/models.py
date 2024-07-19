from app.extensions.db import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(20), default="user")

    tasks = db.relationship(
        "TaskModel", backref="user", lazy=True, cascade="all, delete-orphan"
    )
