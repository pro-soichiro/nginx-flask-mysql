from flaskr.database import db
from datetime import datetime
from sqlalchemy import and_, or_

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, unique=False, default=False)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, from_user_id, to_user_id, message):
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.message = message

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_friend_messages(cls, id1, id2):
        return cls.query.filter(
            or_(
                and_(
                    cls.from_user_id == id1,
                    cls.to_user_id == id2
                ),
                and_(
                    cls.from_user_id == id2,
                    cls.to_user_id == id1
                ),
            )
        ).order_by(cls.create_at).all()

    @classmethod
    def read(cls, ids):
        cls.query.filter(cls.id.in_(ids)).update({cls.is_read: True}, synchronize_session=False)
        db.session.commit()
