from flask import Flask
from flask_migrate import Migrate
from flaskr.database import db
from . import user
from . import blog
from . import auth
from . import main
from . import message
from flaskr.login import login_manager
from flaskr.mail import mail
from flaskr.socketio import socketio
from flaskr.commands.seed import seed

migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.register_blueprint(user.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(message.bp)
    app.config['SECRET_KEY'] = b'\xd3\x8e\xf4<8\xdc\xb3\x8fHb\xd7\x1a\xb1\x98\x16\xbe'
    app.config.from_object('flaskr.config.Config')
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    socketio.init_app(app)
    app.cli.add_command(seed)

    return socketio, app
