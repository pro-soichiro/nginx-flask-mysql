from flask import (
    Blueprint, render_template, request, jsonify, session, redirect, url_for
)
from flaskr.models.user import User
from flaskr.models.user_connect import UserConnect
from flaskr.models.forms import UpdateForm, UserSearchForm, ConnectForm
from flask_login import login_required, current_user
from datetime import datetime
from werkzeug.utils import secure_filename
from flaskr.utils.kakash import Kakash

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

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    user = User.find(id)
    if user is None or current_user.id != id:
        return render_template('not_found.html'), 404
    form = UpdateForm(request.form, obj=user)
    if request.method == 'POST' and form.validate():
        user.name = request.form['name']
        user.email = request.form['email']
        user.birthday = request.form['birthday']
        file = request.files['icon']
        if file:
            ascii_filename = Kakash.japanese_to_ascii(file.filename)
            filename = secure_filename(ascii_filename)
            save_filename = str(user.id) + '_' + str(int(datetime.now().timestamp())) + '_' + filename
            icon_path = 'flaskr/static/images/tmp/' + save_filename
            open(icon_path, 'wb').write(file.read())
            user.icon = 'images/tmp/' + save_filename
            user.save()
        return render_template('user/show.html', user=user)
    return render_template('user/edit.html', form=form)

@bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete(id):
    user = User.find(id)
    if user is None:
        return render_template('not_found.html'), 404
    user.delete()
    return jsonify({ 'status': 'success' })

@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = UserSearchForm(request.form)
    connect_form = ConnectForm()
    session['url'] = 'user.search'

    users = None
    if request.method == 'POST' and form.validate():
        name = form.name.data
        users = User.find_by_name(name)
        print(users)
    return render_template(
        'user/search.html', form=form, users=users, connect_form=connect_form
    )

@bp.route('/connect', methods=['POST'])
@login_required
def connect():
    form = ConnectForm(request.form)
    if request.method == 'POST' and form.validate():
        to_user_id = request.form['to_user_id']
        status = request.form['connect_condition']
        if status == 'accept':
            UserConnect.accept(current_user.id, to_user_id)
        elif status == 'connect':
            UserConnect.connect(current_user.id, to_user_id)
    next_url = session.pop('url', 'main.index')
    return redirect(url_for(next_url))