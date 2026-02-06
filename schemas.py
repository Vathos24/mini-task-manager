from marshmallow import Schema, fields, validate

class TaskSchema(Schema):
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255)
    )
    status = fields.Str(
        validate=validate.OneOf(["pending", "done"])
    )

