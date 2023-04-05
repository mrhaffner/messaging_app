# Updates the model based on button presses, POST results and incoming socketio events
# may need to wait for responses from server for some of the updates
# buttons will general call a method from the controller
# threading may be an issue when communicating with the server
# python modules behave like a singleton

# this controller probably needs to spawn a thread to handle
# listening for the following SocketIO events (see prototype for examples):
#   "message_in" :
#       adds message to MessageList (or updates a sent message to success/fail)
#   "user_change" :
#       updates the UserList
# this should probably be done after a succesful login
# thread is killed on disconnected/logout

import requests
import socketio
import threading as Thread
from model.message import Message, MessageList
from model.user import CurrentUser, User, UserList

API_URL = "http://127.0.0.1:5000"
session = requests.Session()
sio = socketio.Client(http_session=session)
currentUser = CurrentUser()
users = UserList()
messages = MessageList()

# sends account creation details to server so it can save the new account
def create_account(username, password):
    # create user object with username
    user = User(username, password)

    #send user DTO through post
    response = session.post(f"{API_URL}/create_account", json=user.to_dto())

    # handle repsonse code (success/failure)
    # 200 okay
    if response.status_code != 200:
        return False
    
    return True

# sends login POST request to server
# probably spawns a thread to handle/wait for response
# connects via SocketIO after succesful login
# session info will likely be stored on CurrentUser
# updated CurrentUser
def login(username, password):
    # create user object with username
    user = User(username, password)

    #send user DTO through post
    response = session.post(f"{API_URL}/login", json=user.to_dto())
    # handle repsonse code (success/failure)
    # 200 okay
    if response.status_code != 200:
        return False

    try:
        sio.connect(API_URL)
        # sio.register_namespace(MyCustomNamespace(username))
        # sio.emit('join', user.name)
        # sio.namespace = user.name
    except Exception as e:
        print(e)
        return False

    #update current user
    currentUser.add(user, session)
    return True

# accepts message from server
# adds message to model
# for messages
@sio.on("message_out")
def message_in(message_dto):
    messages.add(Message.from_dto(message_dto))


#updating client user list to match what the server sends it
@sio.on("user_change")
def user_change(user_list_dto):
    #user list remove all
    users.remove_all_users()

    #user list add many from dtos
    users.add_many_from_dtos(user_list_dto)

# sends logout POST request to server
# probably spawns a thread to handle/wait for response
# ends SocketIO connection
# sets the CurrentUser to "none" state - (to be defined)
def logout():
    # session.post(url=f"{API_URL}/logout")
    # print(response.status_code)
    # if response.
    # ends SocketIO connection
    sio.disconnect()

    # sets the CurrentUser to "none" state - (to be defined)
    currentUser.remove()

    return True

# sends message via SocketIO "message_out" event
def send_message(text, receiver):
    #check if message is not empty
    if text != "" or receiver.name != "":
        #send message to server
        sio.emit('message_out', Message(text, currentUser._user, receiver).to_dto())


# reconnect via websockets
def reconnect():
    try:
        sio.connect(API_URL)
        return True
    except ConnectionRefusedError:
        return False