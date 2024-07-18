from flask import request
from flask_apispec import use_kwargs, marshal_with, MethodResource
from werkzeug.security import generate_password_hash

from app import db
from app.common.schemas import MessageSchema
from app.modules.user.models import UserModel
from app.modules.auth.schemas import SignUpRequestSchema


class SignUpView(MethodResource):

    @use_kwargs(SignUpRequestSchema, location="json")
    @marshal_with(MessageSchema, code=201)
    @marshal_with(MessageSchema, code=409)
    def post(self, *args, **kwargs):

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
