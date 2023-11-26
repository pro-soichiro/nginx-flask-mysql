from flaskr.database import db
from datetime import datetime
from flask_login import current_user
from sqlalchemy import and_, or_

class UserConnect(db.Model):
    __tablename__ = 'user_connects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Integer, unique=False, default=0)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, from_user_id, to_user_id):
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id

    @classmethod
    def find(cls, from_user_id, to_user_id):
        return cls.query.filter_by(from_user_id=from_user_id, to_user_id=to_user_id).first()

    @classmethod
    def find_room(cls, to_user_id):
        return cls.query.filter(
            or_(
                and_(
                    UserConnect.from_user_id == to_user_id,
                    UserConnect.to_user_id == current_user.id,
                    UserConnect.status == 1
                ),
                and_(
                    UserConnect.from_user_id == current_user.id,
                    UserConnect.to_user_id == to_user_id,
                    UserConnect.status == 1
                )
            ),
        ).first()

    @classmethod
    def accept(cls, current_user_id, to_user_id):
        connect = cls.find(to_user_id, current_user_id)
        if connect is None:
            return False
        connect.status = 1
        connect.save()

    @classmethod
    def connect(cls, from_user_id, to_user_id):
        cls(from_user_id, to_user_id).save()

    @classmethod
    def is_friend(cls, to_user_id):
        user = cls.query.filter(
            or_(
                and_(
                    UserConnect.from_user_id == to_user_id,
                    UserConnect.to_user_id == current_user.id,
                    UserConnect.status == 1
                ),
                and_(
                    UserConnect.from_user_id == current_user.id,
                    UserConnect.to_user_id == to_user_id,
                    UserConnect.status == 1
                )
            ),
        ).first()
        return True if user else False

    def save(self):
        self.update_at = datetime.now()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()