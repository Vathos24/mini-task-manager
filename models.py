from db import db

class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False, default="pending")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status
        }

