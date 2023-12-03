from flaskr.database import db
from datetime import datetime, timedelta
from uuid import uuid4
from flaskr.models.base_model import BaseModel

class PasswordResetToken(BaseModel):
    __tablename__ = 'password_reset_tokens'

    token = db.Column(
        db.String(64),
        unique=True,
        index=True,
        server_default=str(uuid4)
    )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    expire_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, token, user_id, expire_at):
        self.token = token
        self.user_id = user_id
        self.expire_at = expire_at

    @classmethod
    def publish_token(cls, user):
        token = str(uuid4())
        new_token = cls(
            token,
            user.id,
            datetime.now() + timedelta(days=1)
        )
        db.session.add(new_token)
        db.session.commit()
        return token

    @classmethod
    def get_user_id_by_token(cls, token):
        now = datetime.now()
        stmt = (
            db.select(cls.user_id)
            .where(cls.expire_at > now)
            .where(cls.token == str(token))
        )
        user_id = db.session.execute(stmt).scalar()
        return user_id

    @classmethod
    def delete_token(cls, token):
        stmt = db.select(cls).where(cls.token == str(token))
        record = db.session.execute(stmt).scalar()
        db.session.delete(record)
        db.session.commit()
