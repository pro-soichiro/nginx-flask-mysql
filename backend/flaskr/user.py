from flask import Blueprint, render_template
from flaskr.models.user import User
bp = Blueprint('user', __name__, url_prefix='/users')

@bp.route('/')
def index():
    users = User.all()
    return render_template('user/index.html', users=users)

@bp.route('/<int:id>')
def show(id):
    user = User.find(id)
    if user is None:
        return render_template('not_found.html'), 404
    return render_template('user/show.html', user=user)