import pickle

from flask import Flask, request, session
from flask_socketio import emit, disconnect, SocketIO

from model.message import Message
from model.user import User, UserList

# configure and start the app
app = Flask(__name__)
app.secret_key = b"_5#y2L'F4Q8z\n\xec]/"
socketio = SocketIO(app)


@app.route("/create_account", methods=["POST"])
def create_account():
    """Handles account creation from client account information json"""
    data = request.json
    new_user = User.from_dto(data)

    try:
        users.add(new_user)
    except ValueError:
        return "Invalid Credentials", 401

    return "Success", 200


@app.route("/login", methods=["POST"])
def login():
    """Handles user login from client account information json"""
    data = request.json
    user_login = User.from_dto(data)
    user = users.get_user_by_name(user_login.name)  # first need to check if account exists

    if not user or user.password != user_login.password or user.sid != None:
        return "Invalid Credentials", 401

    session["username"] = user_login.name
    return "Success", 200


@app.route("/kick", methods=["POST"])
def kick():
    """Kicks the supplied user"""
    data = request.json
    user = users.get_user_by_name(User.from_dto(data).name)
    disconnect(user.sid, "/")
    return "Success", 200

@socketio.on("message_out")
def messageout(message_dto):
    """
    Socketio "message_out" event to handle messages
    Emits based on "sender/receiver" field
    Group receiver is emitted to everyone
    Otherwise the message is emitted only to the sender (for confirmation) AND receiver
    Emits to "message_in" event
    """
    message = Message.from_dto(message_dto)
    if message.receiver.name == "group":
        message.type = "PM"
        emit("message_out", message.to_dto(), broadcast=True)
    else:
        message.type = "DM"
        receiver_sid = users.get_user_by_name(message.receiver.name).sid
        sender_sid = users.get_user_by_name(message.sender.name).sid
        emit("message_out", message.to_dto(), room=receiver_sid)
        emit("message_out", message.to_dto(), room=sender_sid)
    

@socketio.on("disconnect")
def on_disconnect():
    """
    Needs to handle when a User disconnects from SocketIO (seperate from logout)
    Emits to "user_change" event
    """
    user = users.get_user_by_name(session.get("username"))
    if not user:
        return
    user.sid = None
    session.pop("username", None)
    emit("user_change", users.to_dto(), broadcast=True)


@socketio.on("connect")
def connect():
    """
    Needs to handle when a User first connects via SocketIO
    Emits to "user_change" event for all UserList
    Cannot connect if does not have a session gained from login route
    """
    if session.get("username") is not None:
        user = users.get_user_by_name(session.get("username"))
        if not user:
            return False
        user.sid = request.sid
        emit("user_change", users.to_dto(), broadcast=True)
    else:
        return False
    

# run the app
if __name__ == "__main__":
    try:
        # load existing data
        with open("users.pickle", "rb") as f:
            users = pickle.load(f)
    except:
        # create empty file if does not exist
        with open("users.pickle", "wb") as f:
            users = UserList()
            # create admin superuser
            admin = User(name="admin", password="admin")
            users.add(admin)
            pickle.dump(users, f)

    socketio.run(app)