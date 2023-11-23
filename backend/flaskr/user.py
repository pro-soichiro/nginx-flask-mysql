from flask import Blueprint, render_template, request, jsonify
from flaskr.models.user import User
from flaskr.models.forms import UpdateForm
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

@bp.route('/<int:id>/edit')
def edit(id):
    user = User.find(id)
    if user is None:
        return render_template('not_found.html'), 404
    form = UpdateForm(request.form, obj=user)
    return render_template('user/edit.html', form=form)

@bp.route('/<int:id>', methods=['PATCH'])
def update(id):
    user = User.find(id)
    if user is None:
        return render_template('not_found.html'), 404

    user.name = request.json['name']
    user.email = request.json['email']
    user.birthday = request.json['birthday']
    form = UpdateForm(request.form, obj=user)
    if form.validate():
        user.save()
        return jsonify({ 'status': 'success' })
    else:
        return jsonify({ 'status': 'error', 'errors': form.errors })
