from flaskr.database import db
from sqlalchemy import and_, or_
from flaskr.models.base_model import BaseModel

class UserConnect(BaseModel):
    __tablename__ = 'user_connects'

    from_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Integer, unique=False, default=0)

    def __init__(self, from_user_id, to_user_id):
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id

    @classmethod
    def find_friend(cls, id1, id2):
        return cls.query.filter(
            or_(
                and_(
                    UserConnect.from_user_id == id1,
                    UserConnect.to_user_id == id2,
                    UserConnect.status == 1
                ),
                and_(
                    UserConnect.from_user_id == id2,
                    UserConnect.to_user_id == id1,
                    UserConnect.status == 1
                )
            ),
        ).first()

    @classmethod
    def is_friend(cls, id1, id2):
        user_connect = cls.find_friend(id1, id2)
        return True if user_connect else False

    @classmethod
    def accept(cls, current_user_id, to_user_id):
        connect = cls.query.filter_by(
            from_user_id=to_user_id,
            to_user_id=current_user_id
        ).first()
        if connect is None:
            return False
        connect.status = 1
        connect.save()

    @classmethod
    def connect(cls, from_user_id, to_user_id):
        cls(from_user_id, to_user_id).save()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()