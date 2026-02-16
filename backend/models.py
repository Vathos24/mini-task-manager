from backend.db import db
from datetime import datetime
import json

class Task(db.Model):
    __tablename__ = "tasks"
    __table_args__ = (
        db.Index('idx_tasks_status', 'status'),
        db.Index('idx_tasks_project', 'project'),
        db.Index('idx_tasks_priority', 'priority'),
        db.Index('idx_tasks_created_at', 'created_at'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), nullable=False, default="backlog")
    priority = db.Column(db.String(20), default="medium")
    due_date = db.Column(db.String(50))
    start_time = db.Column(db.String(20))
    end_time = db.Column(db.String(20))
    project = db.Column(db.String(100))
    labels = db.Column(db.String(255))  # Store as comma-separated values
    assignees = db.Column(db.String(255))  # Store as comma-separated values
    attachments = db.Column(db.Text)  # Store as JSON string
    comments = db.Column(db.Text)  # Store as JSON string
    subtasks = db.Column(db.Text)  # Store as JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "due_date": self.due_date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "project": self.project,
            "labels": self.labels.split(',') if self.labels else [],
            "assignees": self.assignees.split(',') if self.assignees else [],
            "attachments": json.loads(self.attachments) if self.attachments else [],
            "comments": json.loads(self.comments) if self.comments else [],
            "subtasks": json.loads(self.subtasks) if self.subtasks else [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
