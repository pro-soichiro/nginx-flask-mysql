from flaskr.database import db

class MessageReadStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=False)
    reader_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_read = db.Column(db.Boolean, default=False)

    @classmethod
    def create(cls, message_id, reader_id):
        read_status = cls(message_id=message_id, reader_id=reader_id)
        db.session.add(read_status)
        db.session.commit()
        return read_status

    @classmethod
    def update(cls, message_id, reader_id):
        read_status = cls.query.filter_by(
            message_id=message_id, reader_id=reader_id).first()
        if read_status:
            read_status.is_read = True
            db.session.commit()
