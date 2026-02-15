import json
from functools import wraps
from flask import jsonify

def handle_list_fields(data):
    """Convert list fields to strings for database storage"""
    for field in ['labels', 'assignees', 'attachments', 'comments', 'subtasks']:
        if field in data and isinstance(data[field], list):
            data[field] = json.dumps(data[field])
    return data

def paginate(query, page=1, per_page=10):
    """Helper function for pagination"""
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    return {
        'items': paginated.items,
        'total': paginated.total,
        'page': page,
        'per_page': per_page,
        'pages': paginated.pages
    }