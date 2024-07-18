from app.modules.auth import init_auth
from app.modules.user import init_user
from app.modules.task import init_task


def init_modules(app):
    init_user(app)
    init_auth(app)
    init_task(app)
