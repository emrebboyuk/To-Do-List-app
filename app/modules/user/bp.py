from flask import Blueprint
from app.modules.user.views import UsersView

user_bp = Blueprint("user", __name__, url_prefix="/user", template_folder="templates")

user_bp.add_url_rule(
    "/",
    view_func=UsersView.as_view("get_all_user_view"),
    methods=["GET"],
)

user_bp.add_url_rule(
    "/<int:user_id>/",
    view_func=UsersView.as_view("get_user_view"),
    methods=["GET"],
)

user_bp.add_url_rule(
    "/<int:user_id>/",
    view_func=UsersView.as_view("put_user_view"),
    methods=["PUT"],
)

user_bp.add_url_rule(
    "/<int:user_id>/",
    view_func=UsersView.as_view("delete_user_view"),
    methods=["DELETE"],
)
