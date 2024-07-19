from marshmallow import Schema, fields
from app.common.schemas import MessageSchema


class SignUpRequestSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class LoginViewRequestSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class AccessTokenResponseSchema(Schema):
    access_token = fields.String()
