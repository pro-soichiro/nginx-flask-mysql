from flask import request, render_template, redirect, url_for, Blueprint
from flaskr.models.user import User
from flaskr.models.forms import CreateForm

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = CreateForm(request.form)
    if request.method == 'GET':
        return render_template('auth/signup.html', form=form)
    elif request.method == 'POST':
        if form.validate():
            user = User(name=form.name.data,
                        email=form.email.data,
                        password=form.password.data,
                        password_confirm=form.password_confirm.data)
            user.save()
            return redirect(url_for('auth.thanks'))
        else:
            return render_template('auth/signup.html', form=form)

@bp.route('/signup/thanks')
def thanks():
    return render_template('auth/thanks.html')