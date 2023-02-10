import requests
import socketio

API_URL = "http://127.0.0.1:5000"
session = requests.Session()

print("enter username: ")
username = input()

response = session.get(url=API_URL)
print(response.text)

response = session.post(url=f"{API_URL}/login/{username}")
print(response.text)

response = session.get(url=API_URL)
print(response.text)

sio = socketio.Client(http_session=session)

sio.connect(API_URL)

@sio.on('receive')
def receiver(data):
    print(data)

print("enter message(\"x\" to quit, \"list\" to list users): ")
message = input()
if message == "list":
    print(session.get(url=f"{API_URL}/list-users").text)
elif message != "x":
    sio.emit('message', message)

while message != "x":
    print("enter message(\"x\" to quit, \"list\" to list users): ")
    message = input()
    if message == "list":
        print(session.get(url=f"{API_URL}/list-users").text)
    elif message != "x":
        sio.emit('message', message)

sio.disconnect()

response = session.post(url=f"{API_URL}/logout")
print(response.text)

response = session.get(url=API_URL)
print(response.text)