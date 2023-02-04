from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
users = []
socketio = SocketIO(app)


@app.route("/login/<name>")
def login(name):
    users.append(name)
    return str(users)


@app.route("/logout/<name>")
def logout(name):
    if name in users:
        users.remove(name)
    return str(users)


@socketio.on('message')
def handle_message(data):
    emit('receive', data, broadcast=True)
    print('received message: ' + data)


if __name__ == '__main__':
    socketio.run(app)