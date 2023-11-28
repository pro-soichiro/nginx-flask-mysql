from flaskr.database import db
from datetime import datetime

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        class_name = self.__class__.__name__
        id_str = f'id={self.id}' if self.id else 'id=None'
        created_at_str = f'created_at={self.created_at}' if self.created_at else 'created_at=None'
        updated_at_str = f'updated_at={self.updated_at}' if self.updated_at else 'updated_at=None'

        return f'<{class_name}({id_str}, {created_at_str}, {updated_at_str})>'