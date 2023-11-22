from flask import Flask
from flask_migrate import Migrate
from flaskr.database import db
from . import user
from . import blog
from . import auth
from . import main

def create_app():
    app = Flask(__name__)

    app.register_blueprint(user.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.config['SECRET_KEY'] = b'\xd3\x8e\xf4<8\xdc\xb3\x8fHb\xd7\x1a\xb1\x98\x16\xbe'
    app.config.from_object('flaskr.config.Config')
    migrate = Migrate(app, db, directory='flaskr/migrations')
    db.init_app(app)

    return app
