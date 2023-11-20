from database import db

class Blog(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))

    def __repr__(self):
        return "<Blog(id='%s', title='%s')>" % (self.id, self.title)

    def all():
        return db.session.query(Blog).all()

    def find(id):
        return db.session.query(Blog).filter(Blog.id == id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, title):
        self.title = title
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()