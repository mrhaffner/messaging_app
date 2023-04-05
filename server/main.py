import pickle
from flask import Flask, request, session
from flask_socketio import SocketIO, emit
from model.message import Message
from model.user import UserList, User

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
socketio = SocketIO(app)


@app.route("/create_account", methods=['POST'])
def create_account():
    data = request.json
    new_user = User.from_dto(data)

    try:
        users.add(new_user)
    except ValueError:
        return "Invalid Credentials", 401

    return "Success", 200

# login route - http POST
# create a User session which will allow one to connect via websockets
@app.route("/login", methods=['POST'])
def login():
    data = request.json
    user_login = User.from_dto(data)

    # first need to check if account exists
    user = users.get_user_by_name(user_login.name)
    if not user or user.password != user_login.password:
        return "Invalid Credentials", 401

    session['username'] = user_login.name
    return "Success", 200


# logout route - http POST
# emits to "user_change" event
# @app.route("/logout", methods=['POST'])
# def logout():
#     users.remove_by_username(session["username"])
#     session.pop("username", None)
#     emit('user_change', users.to_dto(), broadcast=True)
#     return "Success", 200



# socketio "message_out" event to handle messages
# emits based on "sender/receiver" field
# "group" receiver is emitted to everyone
# otherwise the message is emitted only to the sender (for confirmation) AND receiver
# emits to "message_in" event

@socketio.on('message_out')
def messageout(message_dto):
    message = Message.from_dto(message_dto)
    if message.receiver.name == "group":
        message.type = "PM"
        emit("message_out", message.to_dto(), broadcast=True)
    else:
        message.type = "DM"
        receiver_sid = users.get_user_by_name(message.receiver.name).sid
        sender_sid = users.get_user_by_name(message.sender.name).sid
        emit('message_out', message.to_dto(), room=receiver_sid)
        emit('message_out', message.to_dto(), room=sender_sid)
    

# needs to handle when a User disconnects from SocketIO (seperate from logout)
# emits to "user_change" event
#maybe?
@socketio.on('disconnect')
def disconnect():
    users.remove_by_username(session["username"])
    session.pop("username", None)
    emit('user_change', users.to_dto(), broadcast=True)


# needs to handle when a User first connects via SocketIO
# emits to "user_change" event for all UserList
# cannot connect if does not have a session gained from login route
@socketio.on('connect')
def connect():
    if session.get('username') is not None:
        user = users.get_user_by_name(session.get('username'))
        user.sid = request.sid
        emit('user_change', users.to_dto(), broadcast=True)
    else:
        return False
    

if __name__ == "__main__":
    try:
        with open('users.pickle', 'rb') as f:
            users = pickle.load(f)
    except:
    #create empty file if cannot read file for whatever reason
        with open('users.pickle', 'wb') as f:
            users = UserList()
            pickle.dump(users, f)

    socketio.run(app)