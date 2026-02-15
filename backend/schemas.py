from marshmallow import Schema, fields, validate, pre_load

class TaskSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    description = fields.Str(allow_none=True)
    status = fields.Str(validate=validate.OneOf(["backlog", "in_progress", "review", "done"]), missing="backlog")
    priority = fields.Str(validate=validate.OneOf(["high", "medium", "low"]), missing="medium")
    due_date = fields.Str(allow_none=True)
    start_time = fields.Str(allow_none=True)
    end_time = fields.Str(allow_none=True)
    project = fields.Str(allow_none=True)
    labels = fields.List(fields.Str(), missing=[])
    assignees = fields.List(fields.Str(), missing=[])
    attachments = fields.List(fields.Dict(), missing=[])
    comments = fields.List(fields.Dict(), missing=[])
    subtasks = fields.List(fields.Dict(), missing=[])
    
    @pre_load
    def process_lists(self, data, **kwargs):
        # Handle list fields
        for field in ['labels', 'assignees', 'attachments', 'comments', 'subtasks']:
            if field in data and isinstance(data[field], str):
                # If it's a JSON string, parse it
                import json
                try:
                    data[field] = json.loads(data[field])
                except:
                    data[field] = []
        return data