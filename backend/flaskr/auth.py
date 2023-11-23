from flask import request, render_template, redirect, url_for, Blueprint
from flaskr.models.user import User
from flaskr.models.forms import CreateForm, LoginForm
from flask_login import login_user, logout_user

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = CreateForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(name=form.name.data,
                    email=form.email.data,
                    password=form.password.data)
        user.save()
        return redirect(url_for('auth.thanks'))
    return render_template('auth/signup.html', form=form)

@bp.route('/signup/thanks')
def thanks():
    return render_template('auth/thanks.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.find_by_email(form.email.data)
        if user and user.validate_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            if not next:
                next = url_for('main.index')
            return redirect(next)
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))