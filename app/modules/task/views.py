from flask_apispec import MethodResource, use_kwargs, marshal_with

from app.db import db
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

    @use_kwargs(CategorySchema, location="json")
    @marshal_with(MessageSchema, code=201)
    @marshal_with(MessageSchema, code=500)
    def post(self, *args, **kwargs):
        new_category = CategoryModel(**kwargs)

        try:
            db.session.add(new_category)
            db.session.commit()

        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return {"message": f"Category created successfully, task_id: {new_category.id}"}, 201

    @marshal_with(MessageSchema, code=200)
    @marshal_with(MessageSchema, code=500)
    def delete(self, category_id):
        category = CategoryModel.query.get_or_404(category_id)
        try:
            db.session.delete(category)
            db.session.commit()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return {"message": "Category deleted successfully"}, 200


class TasksView(MethodResource):
    schema = TaskViewResponseSchema()

    @marshal_with(schema, code=200)
    @marshal_with(MessageSchema, code=500)
    @marshal_with(MessageSchema, code=404)
    def get(self, task_id=None):
        if task_id:
            self.schema.many = False
            try:
                task = TaskModel.query.get_or_404(task_id)
                if not task:
                    return {"message": "Task not found"}, 404
            except Exception as e:
                return {"message": f"An error occurred: {str(e)}"}, 500
            return task, 200
        else:
            self.schema.many = True
            try:
                tasks = TaskModel.query.all()
                return tasks, 200
            except Exception as e:
                return {"message": f"An error occurred: {str(e)}"}, 500

    @use_kwargs(TaskViewPostRequestSchema, location="json")
    @marshal_with(MessageSchema, code=201)
    @marshal_with(MessageSchema, code=500)
    def post(self, *args, **kwargs):
        new_task = TaskModel(**kwargs)

        try:
            db.session.add(new_task)
            db.session.commit()

        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return {"message": f"Task created successfully, task_id: {new_task.id}"}, 201

    @use_kwargs(TaskViewPutRequestSchema, location="json")
    @marshal_with(MessageSchema, code=200)
    def put(self, *args, task_id, **kwargs):
        task = TaskModel.query.get_or_404(task_id)
        for key, value in kwargs.items():
            setattr(task, key, value)
        db.session.commit()
        return {"message": "Task updated successfully"}, 200

    @marshal_with(MessageSchema, code=200)
    @marshal_with(MessageSchema, code=500)
    def delete(self, task_id):
        task = TaskModel.query.get_or_404(task_id)
        try:
            db.session.delete(task)
            db.session.commit()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        print("done.")
        return {"message": "Task deleted successfully"}, 200
