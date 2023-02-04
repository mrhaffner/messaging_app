import socketio

sio = socketio.Client()

sio.connect('http://localhost:5000')

@sio.on('receive')
def receiver(data):
    print(data)

print("enter message(\"x\" to quit): ")
message = input()
sio.emit('message', message)

while message != "x":
    print("enter message(\"x\" to quit): ")
    message = input()
    sio.emit('message', message)

sio.disconnect()