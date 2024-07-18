from flask import Flask
from app.modules.user import *
from app.modules.user.bp import user_bp


def init_user(app: Flask):
    app.register_blueprint(user_bp)
