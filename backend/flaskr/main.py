from flask import render_template, Blueprint, session
from flaskr.models.forms import ConnectForm
from flaskr.models.user import User
from flask_login import current_user

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    friends = requested_friends = requesting_friends = None
    connect_form = ConnectForm()
    session['url'] = 'main.index'
    if current_user.is_authenticated:
        friends = User.friends()
        requested_friends = User.requested_friends()
        requesting_friends = User.requesting_friends()
    return render_template(
        'index.html',
        friends=friends,
        requested_friends=requested_friends,
        requesting_friends=requesting_friends,
        connect_form=connect_form
    )

@bp.route('/terms')
def terms():
    return render_template('terms.html')

@bp.errorhandler(500)
def internal_server_error(error):
    return render_template('internal_server_error.html'), 500

@bp.errorhandler(404)
def not_found(error):
    return render_template('not_found.html'), 404
