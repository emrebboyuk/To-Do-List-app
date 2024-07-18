from flask import Blueprint
from app.modules.auth.views import SignUpView, LoginView

auth_bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="templates")

auth_bp.add_url_rule(
    "/sign-up/",
    view_func=SignUpView.as_view("sign_up_view"),
    methods=["POST"],
)


auth_bp.add_url_rule(
    "/login/",
    view_func=LoginView.as_view("login_view"),
    methods=["POST"],
)
