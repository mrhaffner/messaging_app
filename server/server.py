from flask import Flask, request, session
from flask_socketio import SocketIO, emit
from server.model import UserList, UserDTO, User, MessageDTO, Message
import json

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
socketio = SocketIO(app)
users = UserList()
msg = Message()

# login route - http POST
# create a user session which will allow one to connect via websockets
# change to json
@app.route("/login", methods=['POST'])
def login():
    data = request.json
    # hopefully works - test
    session['username'] = data.user.name
    return f'logged in as {session["username"]}'


# logout route - http POST
# emits to "user_change" event
@app.route("/logout", methods=['POST'])
def logout():
    users.remove_by_username(session["username"])
    session.pop("username", None)
    emit('user_change', users.to_dto())



# socketio "message_out" event to handle messages
# emits based on "sender/receiver" field
# "group" receiver is emitted to everyone
# otherwise the message is emitted only to the sender (for confirmation) AND receiver
# emits to "message_in" event

@socketio.on('message_out')
def messageout(sender, receiver):
    if User.from_dto(receiver).name == "group":
        emit("message_out", msg.to_dto())
    else:
        emit('message_out', msg.to_dto(), namespace=User.from_dto(sender).name)
        emit('message_out', msg.to_dto(), namespace=User.from_dto(receiver).name)
        
    

# needs to handle when a user disconnects from SocketIO (seperate from logout)
# emits to "user_change" event
#maybe?
@socketio.on('disconnect')
def disconnect():
    users.remove_by_username(session["username"])
    session.pop("username", None)
    emit('user_change', users.to_dto())


# needs to handle when a user first connects via SocketIO
# emits to "user_change" event for all users
# cannot connect if does not have a session gained from login route
@socketio.on('connect')
def connect():
    if request.namespace in session:
        emit('user_change', users.to_dto())
    else:
        return False
    

def main():
    socketio.run(app)

if __name__ == "__main__":
    main()