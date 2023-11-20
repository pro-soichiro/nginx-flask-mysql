from database import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    password_confirm = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer)
    icon = db.Column(db.String(255))
    is_logged_in = db.Column(db.Boolean)
    blogs = db.relationship('Blog', backref='user', lazy=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp(), server_onupdate=db.func.current_timestamp())

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def find(cls, id):
        return cls.query.get(id)

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
