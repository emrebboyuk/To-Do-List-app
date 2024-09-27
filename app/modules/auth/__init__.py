from flask import Flask

from app.modules.auth import *
from app.modules.auth.bp import auth_bp
from app.modules.auth.docs import register_docs


def init_auth(app: Flask):
    app.register_blueprint(auth_bp)
    register_docs()
