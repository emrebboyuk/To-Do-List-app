from app.extensions.docs import docs

from app.modules.auth.views import SignUpView, LoginView


def register_docs():
    docs.register(SignUpView, endpoint="auth.sign_up_view")
    docs.register(LoginView, endpoint="auth.login_view")
