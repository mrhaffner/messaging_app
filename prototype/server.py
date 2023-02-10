from flask import Flask, session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
socketio = SocketIO(app)
users = set()

@app.route("/")
def home():
    if "username" in session:
        return f"logged in as {session['username']}"
    else:
        return "not logged in"

@app.route("/login/<username>", methods=['POST'])
def login(username):
    if username in users:
        return f"username {username} is already taken"
    session['username'] = username
    users.add(username)
    return f'logged in as {session["username"]}'


@app.route("/logout", methods=['POST'])
def logout():
    users.discard(session["username"])
    session.pop("username", None)
    return "logged out"

@app.route("/list-users", methods=['GET'])
def list_users():
    return list(users)

# probably handle auth a bit differently, maybe not allow connection at all to websocket
# don't emit message back to user that sent it (for CLI prototype, probably send ACK to GUI version)
@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)
    if "username" in session:
        print(f"logged in as {session['username']}")
        emit('receive', data, broadcast=True)
    else:
        print("not logged in")
        

if __name__ == '__main__':
    socketio.run(app)