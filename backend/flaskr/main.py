from flask import render_template, Blueprint

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/terms')
def terms():
    return render_template('terms.html')

@bp.errorhandler(500)
def internal_server_error(error):
    return render_template('internal_server_error.html'), 500

@bp.errorhandler(404)
def not_found(error):
    return render_template('not_found.html'), 404
