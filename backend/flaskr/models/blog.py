from flaskr.database import db
from flaskr.models.base_model import BaseModel

class Blog(BaseModel):
    __tablename__ = 'blogs'

    title = db.Column(db.String(255))
    body = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

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
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
