from marshmallow import Schema, fields, validate, pre_load

class TaskSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    description = fields.Str(allow_none=True)
    status = fields.Str(validate=validate.OneOf(["backlog", "in_progress", "review", "done"]))
    priority = fields.Str(validate=validate.OneOf(["high", "medium", "low"]))
    due_date = fields.Str(allow_none=True)
    start_time = fields.Str(allow_none=True)
    end_time = fields.Str(allow_none=True)
    project = fields.Str(allow_none=True)
    labels = fields.List(fields.Str())
    assignees = fields.List(fields.Str())
    attachments = fields.List(fields.Dict())
    comments = fields.List(fields.Dict())
    subtasks = fields.List(fields.Dict())
    
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
            elif field not in data or data[field] is None:
                data[field] = []
        if 'status' not in data or data['status'] is None:
            data['status'] = 'backlog'
        if 'priority' not in data or data['priority'] is None:
            data['priority'] = 'medium'
        return data
