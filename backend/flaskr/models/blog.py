from flaskr.database import db
from datetime import datetime

class Blog(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    body = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return "<Blog(id='%s', title='%s', body='%s')>" % (self.id, self.title, self.body)

    @staticmethod
    def all():
        return db.session.query(Blog).all()

    @staticmethod
    def find(id):
        return db.session.query(Blog).filter(Blog.id == id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, title, body):
        self.title = title
        self.body = body
        self.update_at = datetime.now()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
