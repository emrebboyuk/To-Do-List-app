from flask import Flask
from app.modules.user import *
from app.modules.user.bp import user_bp
from app.modules.user.docs import register_docs


def init_user(app: Flask):
    app.register_blueprint(user_bp)
    register_docs()
