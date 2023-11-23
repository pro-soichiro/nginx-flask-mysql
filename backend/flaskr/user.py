from flask import Blueprint, render_template, request, jsonify
from flaskr.models.user import User
from flaskr.models.forms import UpdateForm
from flask_login import login_required, current_user
from datetime import datetime

bp = Blueprint('user', __name__, url_prefix='/users')

@bp.route('/')
@login_required
def index():
    users = User.all()
    return render_template('user/index.html', users=users)

@bp.route('/<int:id>')
@login_required
def show(id):
    user = User.find(id)
    if user is None:
        return render_template('not_found.html'), 404
    return render_template('user/show.html', user=user)

@bp.route('/<int:id>/edit')
@login_required
def edit(id):
    user = User.find(id)
    if user is None or current_user.id != id:
        return render_template('not_found.html'), 404
    form = UpdateForm(request.form, obj=user)
    return render_template('user/edit.html', form=form)

@bp.route('/<int:id>', methods=['PATCH'])
@login_required
def update(id):
    user = User.find(id)
    if user is None or current_user.id != id:
        return render_template('not_found.html'), 404

    form = UpdateForm(request.form, obj=user)
    if form.validate():
        user.name = request.form['name']
        user.email = request.form['email']
        user.birthday = request.form['birthday']
        file = request.files['icon']
        if file:
            file_name = str(user.id) + '_' + str(int(datetime.now().timestamp())) + '_' + file.filename
            icon_path = 'flaskr/static/images/tmp/' + file_name
            open(icon_path, 'wb').write(file.read())
            user.icon = 'images/tmp/' + file_name
            user.save()
            return jsonify({ 'status': 'success' })
    else:
        return jsonify({ 'status': 'error', 'errors': form.errors })

@bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete(id):
    user = User.find(id)
    if user is None:
        return render_template('not_found.html'), 404
    user.delete()
    return jsonify({ 'status': 'success' })