from marshmallow import Schema, fields
from typing import Type


class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)


class TaskViewResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str()
    due_date = fields.Str()
    completed = fields.Bool()
    category_id = fields.Int(required=True)
    category = fields.Nested(CategorySchema(), dump_only=True)


class TaskViewPostRequestSchema(Schema):
    title = fields.String(required=True)
    description = fields.String()
    due_date = fields.String()
    category_id = fields.Integer(required=True)


class TaskViewPutRequestSchema(Schema):
    title = fields.String()
    description = fields.String()
    due_date = fields.String()
    completed = fields.Boolean()
    category_id = fields.Integer()
