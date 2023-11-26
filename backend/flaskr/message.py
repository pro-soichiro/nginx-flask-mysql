from flask import Blueprint, render_template, request, redirect, url_for
from flaskr.models.message import Message
from flaskr.models.user import User
from flaskr.models.forms import MessageForm
from flaskr.models.user_connect import UserConnect
from flask_login import login_required, current_user
from flaskr.socketio import socketio
from flask_socketio import send, emit, join_room

bp = Blueprint('message', __name__, url_prefix='/messages')

@bp.route('/<int:id>', methods=['GET'])
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
    userConnect = UserConnect.find_room(id)
    return render_template('message/index.html', form=form, messages=messages, user=user, room=userConnect.id)

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    emit('join', current_user.name + ' has entered the room.', to=room)

@socketio.on('message')
def handle_message(data):
    message = data['message']
    to_user_id = data['to_user_id']
    room = data['room']

    # user = User.find(to_user_id)
    # messages = Message.get_friend_messages(current_user.id, to_user_id)
    # read_message_ids = [message.id for message in messages if (not message.is_read) and (message.from_user_id == to_user_id)]
    # if read_message_ids:
    #     Message.read(read_message_ids)
    form = MessageForm(message=message, to_user_id=to_user_id)
    messageData = None
    if form.validate():
        messageData = Message(
            from_user_id=current_user.id,
            to_user_id=to_user_id,
            message=form.message.data
        )
        messageData.save()
    fromUser = User.find(messageData.from_user_id)
    response_data = {
        'message': messageData.message,
        # 'is_read': messageData.is_read,
        'create_at': messageData.create_at.strftime('%H:%M'),
        'user_name': fromUser.name,
        'user_id': fromUser.id
    }
    send(response_data, room=room)
