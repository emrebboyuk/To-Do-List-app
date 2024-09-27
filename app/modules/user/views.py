from flask_apispec import use_kwargs, marshal_with, MethodResource, doc
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from app.extensions.db import db
from app.common.schemas import MessageSchema
from app.modules.user.models import UserModel
from app.modules.user.schemas import UserViewResponseSchema, UserViewPutRequestSchema


class UsersView(MethodResource):
    """
    API endpoint to manage users.

    This view provides multiple user management functionalities:
    - Fetching a user's details (admin or self).
    - Updating a user's details.
    - Deleting a user.

    Permissions:
    - Only admins can view, update, or delete other users' data.
    - Regular users can only view, update, or delete their own data.
    """

    schema = UserViewResponseSchema()

    @doc(
        description="Fetch user details. Admins can access any user, while regular users can access only their own information.",
        tags=["Users"],
    )
    @jwt_required()
    @marshal_with(schema, code=200, description="User data retrieved successfully.")
    @marshal_with(MessageSchema, code=500, description="An error occurred.")
    @marshal_with(MessageSchema, code=404, description="User not found.")
    @marshal_with(MessageSchema, code=403, description="Access denied.")
    def get(self, user_id=None):
        """
        Retrieve user information.

        If `user_id` is provided, fetches that user's information. Admins can access any user's data, while regular users can only access their own.

        Args:
            user_id (int): ID of the user to fetch (optional).

        Returns:
            dict: The user's data or a message indicating the result.
        """
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
                    users = UserModel.query.filter_by(id=current_user_id).all()
                return users, 200
            except Exception as e:
                return {"message": f"An error occurred: {str(e)}"}, 500

    @doc(
        description="Update a user's details. Admins can update any user, while regular users can update only their own data.",
        tags=["Users"],
    )
    @jwt_required()
    @use_kwargs(UserViewPutRequestSchema, location="json")
    @marshal_with(schema, code=201, description="User updated successfully.")
    @marshal_with(MessageSchema, code=500, description="An error occurred.")
    @marshal_with(MessageSchema, code=403, description="Access denied.")
    def put(self, *args, user_id, **kwargs):
        """
        Update user information.

        Allows admins to update any user's data. Regular users can only update their own data.

        Args:
            user_id (int): ID of the user to update.
            *args: Additional arguments.
            **kwargs: User data to update.

        Returns:
            dict: The updated user's data or a message indicating the result.
        """
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

    @doc(
        description="Delete a user. Admins can delete any user, while regular users can delete only their own account.",
        tags=["Users"],
    )
    @jwt_required()
    @marshal_with(MessageSchema, code=200, description="User deleted successfully.")
    @marshal_with(MessageSchema, code=500, description="An error occurred.")
    @marshal_with(MessageSchema, code=403, description="Access denied.")
    def delete(self, user_id):
        """
        Delete a user.

        Allows admins to delete any user. Regular users can only delete their own account.

        Args:
            user_id (int): ID of the user to delete.

        Returns:
            dict: A message indicating the result of the operation.
        """
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
