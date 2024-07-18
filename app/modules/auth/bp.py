from flask import Blueprint
from app.modules.auth.views import SignUpView

auth_bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="templates")

auth_bp.add_url_rule(
    "/sign-up/",
    view_func=SignUpView.as_view("sign_up_view"),
    methods=["POST"],
)
