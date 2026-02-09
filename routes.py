from flask import request, jsonify
from flask_jwt_extended import jwt_required
from models import Task
from db import db
from schemas import TaskSchema
from cache import cache
from auth import login as auth_login
from marshmallow import ValidationError

task_schema = TaskSchema()

def register_routes(app):

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.post("/login")
    def login():
        data = request.get_json() or {}
        token = auth_login(data.get("username"), data.get("password"))
        if not token:
            return jsonify(error="Invalid credentials"), 401
        return jsonify(access_token=token)

    @app.post("/tasks")
    @jwt_required()
    def create_task():
        try:
            data = task_schema.load(request.get_json() or {})
        except ValidationError as err:
            return jsonify(errors=err.messages), 400
        task = Task(**data)
        db.session.add(task)
        db.session.commit()
        return jsonify(task.to_dict()), 201

    @cache.cached(timeout=30, query_string=True)
    @app.get("/tasks")
    @jwt_required()
    def list_tasks():
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)

        tasks = Task.query.paginate(page=page, per_page=limit, error_out=False)
        return jsonify({
            "items": [t.to_dict() for t in tasks.items],
            "total": tasks.total
        })

