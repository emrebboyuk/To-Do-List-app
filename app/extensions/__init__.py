from app.extensions.jwt import jwt
from app.extensions.db import db


def init_extensions(app):
    db.init_app(app)
    jwt.init_app(app)