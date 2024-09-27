from app.extensions.docs import docs

from app.modules.user.views import UsersView


def register_docs():
    docs.register(UsersView, endpoint="user.get_all_user_view")
    docs.register(UsersView, endpoint="user.get_user_view")
    docs.register(UsersView, endpoint="user.put_user_view")
    docs.register(UsersView, endpoint="user.delete_user_view")
