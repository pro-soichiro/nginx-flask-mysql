from flask import Blueprint, render_template, request, redirect, url_for
from flaskr.models.message import Message
from flaskr.models.user import User
from flaskr.models.forms import MessageForm
from flaskr.models.user_connect import UserConnect
from flaskr.models.message_read_status import MessageReadStatus
from flask_login import login_required, current_user
from flaskr.socketio import socketio
from flask_socketio import emit, join_room

bp = Blueprint('message', __name__, url_prefix='/messages')

@bp.route('/<int:to_user_id>', methods=['GET'])
@login_required
def index(to_user_id):
    user_connect = UserConnect.find_friend(current_user.id, to_user_id)
    if not user_connect:
        return redirect(url_for('main.index'))
    form = MessageForm(request.form)
    messages = Message.get_friend_messages(current_user.id, to_user_id)
    return render_template(
        'message/index.html',
        form=form,
        messages=messages,
        to_user_id=to_user_id,
        room_id=user_connect.id,
    )

@socketio.on('join')
def hundle_join(data):
    room = data['room']
    to_user_id = data['to_user_id']
    join_room(room)

    not_read_message_ids = Message.get_not_read_message_ids(current_user.id, to_user_id)
    response_data = {
        'message': current_user.name + ' has entered the room.',
        'not_read_message_ids': not_read_message_ids
    }
    emit('join', response_data, room=room)

@socketio.on('send_message')
def handle_send_message(data):
    message = data['message']
    to_user_id = data['to_user_id']
    room = data['room']

    form = MessageForm(message=message, to_user_id=to_user_id)
    messageData = None
    if form.validate():
        messageData = Message(
            from_user_id=current_user.id,
            to_user_id=to_user_id,
            message=form.message.data
        )
        messageData.save()
        MessageReadStatus.create(messageData.id, to_user_id)

    fromUser = User.find(messageData.from_user_id)
    response_data = {
        'message': {
            'content': messageData.message,
            'id': messageData.id,
            'create_at': messageData.create_at.strftime('%H:%M'),
        },
        'from_user': {
            'name': fromUser.name,
            'icon': fromUser.icon,
            'id': fromUser.id,
        }
    }
    emit('new_message', response_data, room=room)

@socketio.on('read_message')
def handle_read_message(data):
    message_id = data['message_id']
    reader_id = data['reader_id']

    MessageReadStatus.update(message_id, reader_id)

    emit('message_read', {
            'message_id': message_id,
            'reader_id': reader_id
        }, room=data['room'])
