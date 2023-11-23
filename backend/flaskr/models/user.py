from flaskr.database import db
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flaskr.login import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    birthday = db.Column(db.DateTime)
    icon = db.Column(db.String(255))
    is_logged_in = db.Column(db.Boolean)
    blogs = db.relationship('Blog', backref='user', lazy=True)
    is_active = db.Column(db.Boolean, unique=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp(), server_onupdate=db.func.current_timestamp())

    def __init__(self, name, email, password, birthday=None, icon=None, is_logged_in=None):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.birthday = birthday
        self.icon = icon
        self.is_logged_in = is_logged_in

    def validate_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def find(cls, id):
        return cls.query.get(id)

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

        def __repr__(self):
            return f'<User id:{self.id}, name:{self.name}, email:{self.email}, \
                password:{self.password}, password_confirm:{self.password_confirm}, \
                birthday:{self.birthday}, icon:{self.icon}, is_logged_in:{self.is_logged_in}>'

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def age(self):
        if self.birthday is None:
            return None
        today = date.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
