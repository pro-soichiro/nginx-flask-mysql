from flaskr.database import db
from datetime import date, datetime
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from flaskr.login import login_manager
from sqlalchemy.orm import aliased
from sqlalchemy import and_, or_
from flaskr.models.user_connect import UserConnect
from flaskr.models.base_model import BaseModel

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(UserMixin, BaseModel):
    __tablename__ = 'users'

    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(
        db.String(128),
        default=generate_password_hash('snsflaskapp')
    )
    birthday = db.Column(db.DateTime)
    icon = db.Column(
        db.String(255),
        default='images/default_icon.png'
    )
    blogs = db.relationship('Blog', backref='user', lazy=True)
    is_active = db.Column(db.Boolean, unique=False, default=False)

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

    @classmethod
    def find_by_name(cls, name):
        user_connect1 = aliased(UserConnect)
        user_connect2 = aliased(UserConnect)

        return cls.query.filter(
            cls.name.like(f'%{name}%'),
            cls.id != current_user.id,
            cls.is_active == True
        ).outerjoin(
            user_connect1,
            and_(
                user_connect1.from_user_id == cls.id,
                user_connect1.to_user_id == current_user.id
            )
        ).outerjoin(
            user_connect2,
            and_(
                user_connect2.from_user_id == current_user.id,
                user_connect2.to_user_id == cls.id
            )
        ).with_entities(
            cls.id, cls.name, cls.icon,
            user_connect1.status.label('joined_status_to_from'),
            user_connect2.status.label('joined_status_from_to')
        ).all()

    @classmethod
    def friends(cls):
        return cls.query.join(
            UserConnect,
            or_(
                and_(
                    UserConnect.to_user_id == cls.id,
                    UserConnect.from_user_id == current_user.id,
                    UserConnect.status == 1
                ),
                and_(
                    UserConnect.from_user_id == cls.id,
                    UserConnect.to_user_id == current_user.id,
                    UserConnect.status == 1
                )
            )
        ).with_entities(
            cls.id, cls.name, cls.icon
        ).all()

    @classmethod
    def requested_friends(cls):
        return cls.query.join(
            UserConnect,
            and_(
                UserConnect.from_user_id == cls.id,
                UserConnect.to_user_id == current_user.id,
                UserConnect.status == 0
            )
        ).with_entities(
            cls.id, cls.name, cls.icon
        ).all()

    @classmethod
    def requesting_friends(cls):
        return cls.query.join(
            UserConnect,
            and_(
                UserConnect.from_user_id == current_user.id,
                UserConnect.to_user_id == cls.id,
                UserConnect.status == 0
            )
        ).with_entities(
            cls.id, cls.name, cls.icon
        ).all()

    def save(self):
        self.update_at = datetime.now()
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
                        icon:{self.icon}'

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
