from flask import Flask
from app.modules.task import *  # Ask this usage.
from app.modules.task.bp import task_bp, category_bp
from app.modules.task.docs import register_docs


def init_task(app: Flask):
    app.register_blueprint(task_bp)
    app.register_blueprint(category_bp)
    register_docs()
