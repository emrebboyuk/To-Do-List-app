from marshmallow import Schema, fields
from typing import Type
from app.modules.task.schemas import TaskViewResponseSchema as TaskSchema


class UserViewResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    registered_on = fields.DateTime(dump_only=True)
    role = fields.Str(dump_only=True)
    tasks = fields.List(fields.Nested(TaskSchema()), dump_only=True)


class UserViewPutRequestSchema(Schema):
    username = fields.String()
    email = fields.String()
    password = fields.String()
