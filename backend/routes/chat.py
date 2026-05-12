from extensions import socketio, mongo
from flask_socketio import emit, join_room, leave_room
from datetime import datetime

# Basic Socket.IO Events

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join')
def on_join(data):
    room = data.get('room')
    if room:
        join_room(room)
        emit('status', {'msg': f'Someone entered the room {room}.'}, room=room)

@socketio.on('leave')
def on_leave(data):
    room = data.get('room')
    if room:
        leave_room(room)
        emit('status', {'msg': f'Someone left the room {room}.'}, room=room)

@socketio.on('message')
def handle_message(data):
    room = data.get('room')
    senderId = data.get('senderId')
    senderName = data.get('senderName')
    text = data.get('text')
    
    if not all([room, senderId, senderName, text]):
        return
        
    msg_doc = {
        'roomId': room,
        'senderId': senderId,
        'senderName': senderName,
        'text': text,
        'timestamp': datetime.utcnow()
    }
    
    mongo.db.messages.insert_one(msg_doc)
    
    msg_doc['_id'] = str(msg_doc['_id'])
    msg_doc['timestamp'] = msg_doc['timestamp'].isoformat()
    
    emit('message', msg_doc, room=room)
