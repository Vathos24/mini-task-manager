from flask import request, jsonify
from flask_jwt_extended import jwt_required
from models import Task
from db import db
from schemas import TaskSchema

task_schema = TaskSchema()

def register_routes(app):

    @app.post("/tasks")
    @jwt_required()
    def create_task():
        data = task_schema.load(request.json)
        task = Task(**data)
        db.session.add(task)
        db.session.commit()
        return jsonify(task.to_dict()), 201

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
@cache.cached(timeout=30, query_string=True)
@app.get("/tasks")
def list_tasks():
    ...

