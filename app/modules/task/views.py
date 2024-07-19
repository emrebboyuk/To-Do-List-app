from flask_apispec import MethodResource, use_kwargs, marshal_with
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
    schema = CategorySchema()

    @jwt_required()
    @marshal_with(schema, code=200)
    @marshal_with(MessageSchema, code=500)
    def get(self, category_id=None):
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

    @jwt_required()
    @use_kwargs(CategorySchema, location="json")
    @marshal_with(MessageSchema, code=201)
    @marshal_with(MessageSchema, code=500)
    def post(self, *args, **kwargs):
        claims = get_jwt()
        if claims["role"] != "admin":  # i changed this
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

    @jwt_required()
    @marshal_with(MessageSchema, code=200)
    @marshal_with(MessageSchema, code=500)
    def delete(self, category_id):
        claims = get_jwt()
        if claims["role"] != "admin":  # i changed this
            return {"message": "Admin access required"}, 403

        category = CategoryModel.query.get_or_404(category_id)
        try:
            db.session.delete(category)
            db.session.commit()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return {"message": "Category deleted successfully"}, 200


class TasksView(MethodResource):
    schema = TaskViewResponseSchema()

    @jwt_required()
    @marshal_with(schema, code=200)
    @marshal_with(MessageSchema, code=500)
    @marshal_with(MessageSchema, code=404)
    @marshal_with(MessageSchema, code=403)
    def get(self, task_id=None):
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        user_role = claims["role", "user"]

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

    @jwt_required()
    @use_kwargs(TaskViewPostRequestSchema, location="json")
    @marshal_with(MessageSchema, code=201)
    @marshal_with(MessageSchema, code=500)
    def post(self, *args, **kwargs):
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

    @jwt_required()
    @use_kwargs(TaskViewPutRequestSchema, location="json")
    @marshal_with(MessageSchema, code=200)
    @marshal_with(MessageSchema, code=403)
    def put(self, *args, task_id, **kwargs):
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        user_role = claims["role", "user"]

        task = TaskModel.query.get_or_404(task_id)

        if user_role != "admin" and task.user_id != current_user_id:  # i changed this
            return {"message": "Access denied"}, 403

        for key, value in kwargs.items():
            setattr(task, key, value)
        db.session.commit()
        return {"message": "Task updated successfully"}, 200

    @jwt_required()
    @marshal_with(MessageSchema, code=200)
    @marshal_with(MessageSchema, code=500)
    @marshal_with(MessageSchema, code=403)
    def delete(self, task_id):
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        user_role = claims["role", "user"]

        task = TaskModel.query.get_or_404(task_id)

        if user_role != "admin" and task.user_id != current_user_id:  # i changed this
            return {"message": "Access denied"}, 403

        try:
            db.session.delete(task)
            db.session.commit()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        print("done.")
        return {"message": "Task deleted successfully"}, 200
