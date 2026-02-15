from flask import request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import Task
from backend.db import db
from backend.schemas import TaskSchema
from backend.cache import cache
from backend.auth import login as auth_login
from marshmallow import ValidationError
from backend.utils import handle_list_fields, paginate
import json
import os

task_schema = TaskSchema()

def register_routes(app):

    @app.get('/health')
    def health():
        return jsonify({'status': 'ok', 'message': 'TaskPulse API is running'})

    # Auth endpoints
    @app.post('/api/login')
    def login():
        data = request.get_json() or {}
        token = auth_login(data.get('username'), data.get('password'))
        if not token:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        return jsonify({
            'access_token': token,
            'user': {
                'name': 'Sarah Chen',
                'email': 'sarah@taskpulse.com',
                'role': 'Product Manager',
                'avatar': 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-1.2.1&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80'
            }
        })

    @app.post('/api/logout')
    @jwt_required()
    def logout():
        # In a real app, you might blacklist the token
        return jsonify({'message': 'Logged out successfully'})

    # Task endpoints
    @app.post('/api/tasks')
    @jwt_required()
    def create_task():
        try:
            data = request.get_json() or {}
            # Validate with schema
            validated_data = task_schema.load(data)
            
            # Handle list fields
            db_data = handle_list_fields(validated_data.copy())
            
            task = Task(**db_data)
            db.session.add(task)
            db.session.commit()
            
            # Clear cache
            cache.clear()
            
            return jsonify(task.to_dict()), 201
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.get('/api/tasks')
    @jwt_required()
    @cache.cached(timeout=30, query_string=True)
    def list_tasks():
        try:
            page = request.args.get('page', 1, type=int)
            limit = request.args.get('limit', 20, type=int)
            status = request.args.get('status')
            project = request.args.get('project')
            priority = request.args.get('priority')
            
            query = Task.query
            
            # Apply filters
            if status:
                query = query.filter(Task.status == status)
            if project:
                query = query.filter(Task.project == project)
            if priority:
                query = query.filter(Task.priority == priority)
            
            # Order by created_at descending
            query = query.order_by(Task.created_at.desc())
            
            result = paginate(query, page, limit)
            
            return jsonify({
                'items': [task.to_dict() for task in result['items']],
                'total': result['total'],
                'page': result['page'],
                'per_page': result['per_page'],
                'pages': result['pages']
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.get('/api/tasks/<int:task_id>')
    @jwt_required()
    def get_task(task_id):
        task = Task.query.get_or_404(task_id)
        return jsonify(task.to_dict())

    @app.put('/api/tasks/<int:task_id>')
    @jwt_required()
    def update_task(task_id):
        task = Task.query.get_or_404(task_id)
        
        try:
            data = request.get_json() or {}
            validated_data = task_schema.load(data, partial=True)
            
            # Handle list fields
            db_data = handle_list_fields(validated_data)
            
            for key, value in db_data.items():
                setattr(task, key, value)
            
            db.session.commit()
            cache.clear()
            
            return jsonify(task.to_dict())
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.delete('/api/tasks/<int:task_id>')
    @jwt_required()
    def delete_task(task_id):
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        cache.clear()
        return jsonify({'message': 'Task deleted successfully'})

    @app.patch('/api/tasks/<int:task_id>/status')
    @jwt_required()
    def update_task_status(task_id):
        task = Task.query.get_or_404(task_id)
        data = request.get_json() or {}
        
        new_status = data.get('status')
        if new_status not in ['backlog', 'in_progress', 'review', 'done']:
            return jsonify({'error': 'Invalid status'}), 400
        
        task.status = new_status
        db.session.commit()
        cache.clear()
        
        return jsonify(task.to_dict())

    # Comments endpoints
    @app.post('/api/tasks/<int:task_id>/comments')
    @jwt_required()
    def add_comment(task_id):
        task = Task.query.get_or_404(task_id)
        data = request.get_json() or {}
        
        comment = {
            'id': len(task.comments) + 1,
            'user': get_jwt_identity(),
            'text': data.get('text'),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        comments = task.comments
        comments.append(comment)
        task.comments = json.dumps(comments)
        db.session.commit()
        
        return jsonify(comment), 201

    # Subtasks endpoints
    @app.post('/api/tasks/<int:task_id>/subtasks')
    @jwt_required()
    def add_subtask(task_id):
        task = Task.query.get_or_404(task_id)
        data = request.get_json() or {}
        
        subtask = {
            'id': len(task.subtasks) + 1,
            'title': data.get('title'),
            'completed': False
        }
        
        subtasks = task.subtasks
        subtasks.append(subtask)
        task.subtasks = json.dumps(subtasks)
        db.session.commit()
        
        return jsonify(subtask), 201

    # Dashboard stats
    @app.get('/api/stats')
    @jwt_required()
    @cache.cached(timeout=60)
    def get_stats():
        total_tasks = Task.query.count()
        tasks_by_status = {
            'backlog': Task.query.filter_by(status='backlog').count(),
            'in_progress': Task.query.filter_by(status='in_progress').count(),
            'review': Task.query.filter_by(status='review').count(),
            'done': Task.query.filter_by(status='done').count()
        }
        
        return jsonify({
            'total_tasks': total_tasks,
            'by_status': tasks_by_status
        })