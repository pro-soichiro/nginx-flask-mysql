from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'ログインしてください'

def init_app(app):
    login_manager.init_app(app)