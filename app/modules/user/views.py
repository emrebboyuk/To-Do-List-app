from flask_apispec import use_kwargs, marshal_with, MethodResource
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required

from app.extensions.db import db
from app.common.schemas import MessageSchema
from app.modules.user.models import UserModel
from app.modules.user.schemas import UserViewResponseSchema, UserViewPutRequestSchema


class UsersView(MethodResource):
    schema = UserViewResponseSchema()

    @marshal_with(schema, code=200)
    @marshal_with(MessageSchema, code=500)
    @marshal_with(MessageSchema, code=404)
    def get(self, user_id=None):
        if user_id:
            self.schema.many = False
            try:
                user = UserModel.query.get_or_404(user_id)
                if not user:
                    return {"message": "User not found"}, 404
            except Exception as e:
                return {"message": f"An error occurred: {str(e)}"}, 500
            return user, 200
        else:
            self.schema.many = True
            try:
                users = UserModel.query.all()
                return users, 200
            except Exception as e:
                return {"message": f"An error occurred: {str(e)}"}, 500

    @use_kwargs(UserViewPutRequestSchema, location="json")
    @marshal_with(schema, code=201)
    @marshal_with(MessageSchema, code=500)
    def put(self, *args, user_id, **kwargs):
        user = UserModel.query.get_or_404(user_id)
        try:
            for key, value in kwargs.items():
                if key == "password":
                    value = generate_password_hash(value, method="pbkdf2:sha256")
                setattr(user, key, value)
            db.session.commit()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500
        return user, 201

    @jwt_required()
    @marshal_with(MessageSchema, code=200)
    @marshal_with(MessageSchema, code=500)
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id, description="User not found")
        db.session.delete(user)
        db.session.commit()

        return {"message": "User deleted successfully"}, 200
