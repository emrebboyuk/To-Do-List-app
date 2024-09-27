from flask_apispec import MethodResource, use_kwargs, marshal_with, doc
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from app.extensions.db import db
from app.common.schemas import MessageSchema
from app.modules.task.models import CategoryModel, TaskModel
from app.modules.task.schemas import (
    CategorySchema,
    TaskViewResponseSchema,
    TaskViewPostRequestSchema,
    TaskViewPutRequestSchema,
)


class CategoryView(MethodResource):
    """
    API endpoint to manage task categories.

    This view provides functionalities for category management:
    - Fetching categories (single or multiple).
    - Creating a new category (Admin only).
    - Deleting a category (Admin only).

    Permissions:
    - Only admins can create or delete categories.
    - All users can fetch categories.
    """

    schema = CategorySchema()

    @doc(
        description="Fetch category details. Admins and regular users can access category information.",
        tags=["Categories"],
    )
    @jwt_required()
    @marshal_with(schema, code=200, description="Category retrieved successfully.")
    @marshal_with(MessageSchema, code=500, description="An error occurred.")
    def get(self, category_id=None):
        """
        Retrieve category information.

        If `category_id` is provided, fetches that category's information. If not, returns a list of all categories.

        Args:
            category_id (int): ID of the category to fetch (optional).

        Returns:
            dict: The category's data or a list of categories.
        """
        if category_id:
            self.schema.many = False
            try:
                category = CategoryModel.query.get_or_404(category_id)
            except Exception as e:
                return {"message": f"An error occurred: {str(e)}"}, 500
            return category, 200

        else:
            self.schema.many = True
            categories = CategoryModel.query.all()
            return categories, 200

    @doc(
        description="Create a new category. Only admins can create categories.",
        tags=["Categories"],
    )
    @jwt_required()
    @use_kwargs(CategorySchema, location="json")
    @marshal_with(MessageSchema, code=201, description="Category created successfully.")
    @marshal_with(MessageSchema, code=500, description="An error occurred.")
    def post(self, *args, **kwargs):
        """
        Create a new category.

        Only admins can create new categories.

        Args:
            *args: Additional arguments.
            **kwargs: Category data.

        Returns:
            dict: A message indicating the result.
        """
        claims = get_jwt()
        if claims["role"] != "admin":
            return {"message": "Admin access required"}, 403

        new_category = CategoryModel(**kwargs)
        try:
            db.session.add(new_category)
            db.session.commit()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return {
            "message": f"Category created successfully, task_id: {new_category.id}"
        }, 201

    @doc(
        description="Delete a category. Only admins can delete categories.",
        tags=["Categories"],
    )
    @jwt_required()
    @marshal_with(MessageSchema, code=200, description="Category deleted successfully.")
    @marshal_with(MessageSchema, code=500, description="An error occurred.")
    def delete(self, category_id):
        """
        Delete a category.

        Only admins can delete categories.

        Args:
            category_id (int): ID of the category to delete.

        Returns:
            dict: A message indicating the result.
        """
        claims = get_jwt()
        if claims["role"] != "admin":
            return {"message": "Admin access required"}, 403

        category = CategoryModel.query.get_or_404(category_id)
        try:
            db.session.delete(category)
            db.session.commit()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return {"message": "Category deleted successfully"}, 200


class TasksView(MethodResource):
    """
    API endpoint to manage tasks.

    This view provides functionalities for task management:
    - Fetching a task or all tasks.
    - Creating a new task.
    - Updating a task.
    - Deleting a task.

    Permissions:
    - Admins can view, update, or delete any task.
    - Regular users can only manage their own tasks.
    """

    schema = TaskViewResponseSchema()

    @doc(
        description="Fetch task details. Admins can view any task, while regular users can view only their own tasks.",
        tags=["Tasks"],
    )
    @jwt_required()
    @marshal_with(schema, code=200, description="Task data retrieved successfully.")
    @marshal_with(MessageSchema, code=500, description="An error occurred.")
    @marshal_with(MessageSchema, code=404, description="Task not found.")
    @marshal_with(MessageSchema, code=403, description="Access denied.")
    def get(self, task_id=None):
        """
        Retrieve task information.

        If `task_id` is provided, fetches that task's information. Admins can access any task, while regular users can only access their own.

        Args:
            task_id (int): ID of the task to fetch (optional).

        Returns:
            dict: The task's data or a list of tasks.
        """
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        user_role = claims["role"]

        if task_id:
            self.schema.many = False
            try:
                task = TaskModel.query.get_or_404(task_id)
                if user_role != "admin" and task.user_id != current_user_id:
                    return {"message": "Access denied"}, 403
                if not task:
                    return {"message": "Task not found"}, 404
            except Exception as e:
                return {"message": f"An error occurred: {str(e)}"}, 500
            return task, 200
        else:
            self.schema.many = True
            try:
                if user_role == "admin":
                    tasks = TaskModel.query.all()
                else:
                    tasks = TaskModel.query.filter_by(user_id=current_user_id).all()
                return tasks, 200
            except Exception as e:
                return {"message": f"An error occurred: {str(e)}"}, 500

    @doc(
        description="Create a new task. Regular users can create tasks for themselves.",
        tags=["Tasks"],
    )
    @jwt_required()
    @use_kwargs(TaskViewPostRequestSchema, location="json")
    @marshal_with(MessageSchema, code=201, description="Task created successfully.")
    @marshal_with(MessageSchema, code=500, description="An error occurred.")
    def post(self, *args, **kwargs):
        """
        Create a new task.

        Regular users can create tasks only for themselves.

        Args:
            *args: Additional arguments.
            **kwargs: Task data.

        Returns:
            dict: A message indicating the result.
        """
        current_user_id = get_jwt_identity()

        new_task = TaskModel(
            title=kwargs.get("title"),
            description=kwargs.get("description"),
            due_date=kwargs.get("due_date"),
            category_id=kwargs.get("category_id"),
            user_id=current_user_id,
        )

        try:
            db.session.add(new_task)
            db.session.commit()

        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return {"message": f"Task created successfully, task_id: {new_task.id}"}, 201

    @doc(
        description="Update a task. Admins can update any task, while regular users can only update their own tasks.",
        tags=["Tasks"],
    )
    @jwt_required()
    @use_kwargs(TaskViewPutRequestSchema, location="json")
    @marshal_with(MessageSchema, code=200, description="Task updated successfully.")
    @marshal_with(MessageSchema, code=403, description="Access denied.")
    def put(self, *args, task_id, **kwargs):
        """
        Update task information.

        Admins can update any task, while regular users can update only their own tasks.

        Args:
            task_id (int): ID of the task to update.
            *args: Additional arguments.
            **kwargs: Task data to update.

        Returns:
            dict: A message indicating the result.
        """
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        user_role = claims["role"]

        task = TaskModel.query.get_or_404(task_id)

        if user_role != "admin" and task.user_id != current_user_id:
            return {"message": "Access denied"}, 403

        for key, value in kwargs.items():
            setattr(task, key, value)
        db.session.commit()
        return {"message": "Task updated successfully"}, 200

    @doc(
        description="Delete a task. Admins can delete any task, while regular users can delete only their own tasks.",
        tags=["Tasks"],
    )
    @jwt_required()
    @marshal_with(MessageSchema, code=200, description="Task deleted successfully.")
    @marshal_with(MessageSchema, code=500, description="An error occurred.")
    @marshal_with(MessageSchema, code=403, description="Access denied.")
    def delete(self, task_id):
        """
        Delete a task.

        Admins can delete any task, while regular users can delete only their own tasks.

        Args:
            task_id (int): ID of the task to delete.

        Returns:
            dict: A message indicating the result.
        """
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        user_role = claims["role"]

        task = TaskModel.query.get_or_404(task_id)

        if user_role != "admin" and task.user_id != current_user_id:
            return {"message": "Access denied"}, 403

        try:
            db.session.delete(task)
            db.session.commit()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return {"message": "Task deleted successfully"}, 200
