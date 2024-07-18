from flask import Blueprint
from app.modules.task.views import TasksView, CategoryView

task_bp = Blueprint("task", __name__, url_prefix="/task", template_folder="templates")
category_bp = Blueprint(
    "category", __name__, url_prefix="/category", template_folder="templates"
)


# Category routes

category_bp.add_url_rule(
    "/",
    view_func=CategoryView.as_view("get_all_category_view"),
    methods=["GET"],
)

category_bp.add_url_rule(
    "/<int:category_id>/",
    view_func=CategoryView.as_view("get_category_view"),
    methods=["GET"],
)

category_bp.add_url_rule(
    "/",
    view_func=CategoryView.as_view("post_category_view"),
    methods=["POST"],
)

category_bp.add_url_rule(
    "/<int:category_id>/",
    view_func=CategoryView.as_view("delete_category_view"),
    methods=["DELETE"],
)

# Task routes

task_bp.add_url_rule(
    "/",
    view_func=TasksView.as_view("get_all_task_view"),
    methods=["GET"],
)

task_bp.add_url_rule(
    "/<int:task_id>/",
    view_func=TasksView.as_view("get_task_view"),
    methods=["GET"],
)

task_bp.add_url_rule(
    "/",
    view_func=TasksView.as_view("post_task_view"),
    methods=["POST"],
)

task_bp.add_url_rule(
    "/<int:task_id>/",
    view_func=TasksView.as_view("put_task_view"),
    methods=["PUT"],
)

task_bp.add_url_rule(
    "/<int:task_id>/",
    view_func=TasksView.as_view("delete_task_view"),
    methods=["DELETE"],
)
