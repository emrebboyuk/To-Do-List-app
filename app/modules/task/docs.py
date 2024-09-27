from app.extensions.docs import docs

from app.modules.task.views import CategoryView, TasksView


def register_docs():
    # Categories
    docs.register(CategoryView, endpoint="category.get_all_category_view")
    docs.register(CategoryView, endpoint="category.get_category_view")
    docs.register(CategoryView, endpoint="category.post_category_view")
    docs.register(CategoryView, endpoint="category.delete_category_view")

    # Tasks
    docs.register(TasksView, endpoint="task.get_all_task_view")
    docs.register(TasksView, endpoint="task.get_task_view")
    docs.register(TasksView, endpoint="task.post_task_view")
    docs.register(TasksView, endpoint="task.put_task_view")
    docs.register(TasksView, endpoint="task.delete_task_view")
