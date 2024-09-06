from app.extensions.jwt import jwt
from app.extensions.db import db
from app.extensions.docs import docs


def init_extensions(app):
    db.init_app(app)
    jwt.init_app(app)
    docs.init_app(app)
