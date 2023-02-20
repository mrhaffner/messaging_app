from flask import Flask, session
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
@app.route("/login/<username>", methods=['POST'])
def login(username):
    session['username'] = username
    users.add(username)


# logout route - http POST
# emits to "user_change" event
# maybe ends the user session?
@app.route("/logout", methods=['POST'])
def logout():
    users.remove(session["username"])
    session.pop("username", None)
    emit('user_change', users.to_dto())



# socketio "message_out" event to handle messages
# emits based on "sender/receiver" field
# "group" receiver is emitted to everyone
# otherwise the message is emitted only to the sender (for confirmation) AND receiver
# emits to "message_in" event

@socketio.on('message_out')
def messageout(sender, receiver):
    if receiver == "group":
        emit("message_out", msg.to_dto())
    else:
        # not required but check if user is real?
        for user in users.get_all():
            if user == receiver:
                sender.emit('message_out', msg.to_dto())
                user.emit('message_out', msg.to_dto())
        
    

# needs to handle when a user disconnects from SocketIO (seperate from logout)
# emits to "user_change" event
#maybe?
@socketio.on('disconnect')
def disconnect():
    emit('user_change', users.to_dto())


# needs to handle when a user first connects via SocketIO
# emits to "user_change" event but ONLY for that user
# cannot connect if does not have a session gained from login route
@socketio.on('connect')
def connect(user):
    if users.exist(user):
        user.emit('user_change', users.to_dto())
    else:
        # refuse connection
        pass
    

def main():
    socketio.run(app)

if __name__ == "__main__":
    main()