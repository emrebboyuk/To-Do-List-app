from flask_apispec import use_kwargs, marshal_with, MethodResource
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from app.extensions.db import db
from app.common.schemas import MessageSchema
from app.modules.user.models import UserModel
from app.modules.user.schemas import UserViewResponseSchema, UserViewPutRequestSchema


class UsersView(MethodResource):
    schema = UserViewResponseSchema()

    @jwt_required()
    @marshal_with(schema, code=200)
    @marshal_with(MessageSchema, code=500)
    @marshal_with(MessageSchema, code=404)
    @marshal_with(MessageSchema, code=403)
    def get(self, user_id=None):
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        user_role = claims["role"]

        if user_id:
            self.schema.many = False
            try:
                user = UserModel.query.get_or_404(user_id)
                if not user:
                    return {"message": "User not found"}, 404
                elif user_role != "admin" or user_id != current_user_id:
                    return {"message": "Access denied"}, 403
            except Exception as e:
                return {"message": f"An error occurred: {str(e)}"}, 500
            return user, 200
        else:
            self.schema.many = True
            try:
                if user_role == "admin":
                    users = UserModel.query.all()
                else:
                    users = UserModel.query.filter_by(id=current_user_id).fetchone()
                return users, 200
            except Exception as e:
                return {"message": f"An error occurred: {str(e)}"}, 500

    @jwt_required()
    @use_kwargs(UserViewPutRequestSchema, location="json")
    @marshal_with(schema, code=201)
    @marshal_with(MessageSchema, code=500)
    @marshal_with(MessageSchema, code=403)
    def put(self, *args, user_id, **kwargs):
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        user_role = claims["role"]

        if user_role != "admin" and user_id != current_user_id:
            return {"message": "Access denied"}, 403

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
    @marshal_with(MessageSchema, code=403)
    def delete(self, user_id):
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        user_role = claims["role"]

        if user_role != "admin" and user_id != current_user_id:
            return {"message": "Access denied"}, 403

        user = UserModel.query.get_or_404(user_id, description="User not found")

        try:
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        return {"message": "User deleted successfully"}, 200


def create_admin_user(username, email, password):
    """
    Creates an admin user.
    :param username: username
    :param email: email
    :param password: password
    :return: UserModel object
    """
    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

    new_user = UserModel(
        username=username, email=email, password=hashed_password, role="admin"
    )

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"An error occurred while creating the admin user: {str(e)}")

    return new_user
