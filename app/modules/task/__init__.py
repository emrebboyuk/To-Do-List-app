from flask import Flask
from app.modules.task import *
from app.modules.task.bp import task_bp, category_bp


def init_task(app: Flask):
    app.register_blueprint(task_bp)
    app.register_blueprint(category_bp)
