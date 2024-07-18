import os

from flask import Flask
from dotenv import load_dotenv

# import secrets

from app.db import db
from app.modules import init_modules
from app.modules.user.models import UserModel
from app.modules.task.models import TaskModel, CategoryModel


def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    init_modules(app)

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
