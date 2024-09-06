from flask_apispec import use_kwargs, marshal_with, MethodResource, doc
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from app.extensions.db import db
from app.common.schemas import MessageSchema
from app.modules.user.models import UserModel
from app.modules.auth.schemas import (
    AccessTokenResponseSchema,
    SignUpRequestSchema,
    LoginViewRequestSchema,
)


class SignUpView(MethodResource):
    """
    API endpoint to sign up a new user.

    This view handles the user registration process. It accepts a username, email,
    and password, checks if the user already exists, and creates a new user if the
    credentials are unique.

    Returns:
        201: If the user is created successfully.
        409: If the user with the provided username or email already exists.
    """

    @doc(description="Sign up a new user.", tags=["Authentication"])
    @use_kwargs(SignUpRequestSchema, location="json")
    @marshal_with(MessageSchema, code=201, description="User created successfully.")
    @marshal_with(MessageSchema, code=409, description="User already exists.")
    def post(self, *args, **kwargs):
        """
        Handle user registration.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments containing user data.

        Returns:
            dict: A message indicating the result of the operation.
        """
        if (
                UserModel.query.filter_by(username=kwargs["username"]).first()
                or UserModel.query.filter_by(email=kwargs["email"]).first()
        ):
            return {"message": "User already exists"}, 409

        user = UserModel(
            username=kwargs["username"],
            email=kwargs["email"],
            password=generate_password_hash(
                password=kwargs["password"], method="pbkdf2:sha256"
            ),
        )
        db.session.add(user)
        db.session.commit()
        return {
            "message": "User created successfully",
        }, 201


class LoginView(MethodResource):
    """
    API endpoint to log in a user and provide an access token.

    This view handles user login by checking the provided credentials (username and password).
    If the credentials are correct, it returns a JWT access token.

    Returns:
        200: If the login is successful, with an access token.
        401: If the credentials are invalid.
    """

    @doc(description="Login a user and retrieve an access token.", tags=["Authentication"])
    @use_kwargs(LoginViewRequestSchema, location="json")
    @marshal_with(AccessTokenResponseSchema, code=200, description="Login successful.")
    @marshal_with(MessageSchema, code=401, description="Invalid credentials.")
    def post(self, *args, **kwargs):
        """
        Handle user login.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments containing login data.

        Returns:
            dict: A message indicating the result of the operation.
        """
        user = UserModel.query.filter_by(username=kwargs["username"]).first()

        if not user or not check_password_hash(user.password, kwargs["password"]):
            return {"message": "Invalid credentials"}, 401

        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}, 200
