from database import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    password_confirm = db.Column(db.String(255))
    age = db.Column(db.Integer)
    icon = db.Column(db.String(255))
    is_logged_in = db.Column(db.Boolean)

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def find(cls, id):
        return cls.query.filter_by(id=id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<User id:{}, name:{}, email:{}, password:{}, password_confirm:{}, age:{}, icon:{}, is_logged_in:{}>'.format(
            self.id,
            self.name,
            self.email,
            self.password,
            self.password_confirm,
            self.age,
            self.icon,
            self.is_logged_in
        )
