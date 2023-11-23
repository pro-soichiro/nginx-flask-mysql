from flask import request, render_template, redirect, url_for, Blueprint, flash
from flaskr.database import db
from flaskr.models.user import User
from flaskr.models.password_reset_token import PasswordResetToken
from flaskr.models.forms import CreateForm, LoginForm, ResetPasswordForm
from flask_login import login_user, logout_user

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = CreateForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(name=form.name.data,
                    email=form.email.data)
        user.save()
        token = PasswordResetToken.publish_token(user)
        # shuold be send email
        print(f'###### Publish token: http://localhost/auth/reset_password/{token}')
        flash('Please check your email.')
        return redirect(url_for('auth.thanks'))
    return render_template('auth/signup.html', form=form)

@bp.route('/reset_password/<uuid:token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm(request.form)
    reset_user_id = PasswordResetToken.get_user_id_by_token(token)
    if reset_user_id is None:
        return render_template('not_found.html'), 404
    elif request.method == 'POST' and form.validate():
        password = form.password.data
        user = User.find(reset_user_id)
        user.save_new_password(password)
        PasswordResetToken.delete_token(token)
        flash('Password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

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