from flask import Flask, session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
socketio = SocketIO(app)

@app.route("/")
def home():
    if "username" in session:
        return f"logged in as {session['username']}"
    else:
        return "not logged in"

@app.route("/login/<username>", methods=['POST'])
def login(username):
    session['username'] = username
    return f'logged in as {session["username"]}'


@app.route("/logout", methods=['POST'])
def logout():
    session.pop("username", None)
    return "logged out"


# probably handle auth a bit differently, maybe not allow connection at all to websocket
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