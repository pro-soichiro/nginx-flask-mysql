from flaskr.database import db
from datetime import date, datetime
from flask_bcrypt import generate_password_hash, check_password_hash
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
    password = db.Column(
        db.String(128),
        default=generate_password_hash('snsflaskapp')
    )
    birthday = db.Column(db.DateTime)
    icon = db.Column(db.String(255))
    is_logged_in = db.Column(db.Boolean)
    blogs = db.relationship('Blog', backref='user', lazy=True)
    is_active = db.Column(db.Boolean, unique=False, default=False)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, name, email):
        self.name = name
        self.email = email

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

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<User  id:{self.id}, \
                        name:{self.name}, \
                        email:{self.email}, \
                        password:{self.password} \
                        birthday:{self.birthday}, \
                        icon:{self.icon}, \
                        is_logged_in:{self.is_logged_in}>'

    def save_new_password(self, new_password):
        self.password = generate_password_hash(new_password)
        self.is_active = True
        db.session.add(self)
        db.session.commit()

    @property
    def age(self):
        if self.birthday is None:
            return None
        today = date.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
