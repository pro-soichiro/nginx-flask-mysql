from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flaskr.models.message import Message
from flaskr.models.user import User
from flaskr.models.forms import MessageForm
from flaskr.models.user_connect import UserConnect
from flask_login import login_required, current_user

bp = Blueprint('message', __name__, url_prefix='/messages')

@bp.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def index(id):
    if not UserConnect.is_friend(id):
        return redirect(url_for('main.index'))
    form = MessageForm(request.form)
    messages = Message.get_friend_messages(current_user.id, id)
    user = User.find(id)
    read_message_ids = [message.id for message in messages if (not message.is_read) and (message.from_user_id == id)]
    if read_message_ids:
        Message.read(read_message_ids)
    if request.method == 'POST' and form.validate():
        message = Message(
            from_user_id=current_user.id,
            to_user_id=id,
            message=form.message.data
        )
        message.save()
        return redirect(url_for('message.index', id=id))
    return render_template('message/index.html', form=form, messages=messages, user=user)