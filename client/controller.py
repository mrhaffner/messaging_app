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

# sends login POST request to server
# probably spawns a thread to handle/wait for response
# connects via SocketIO after succesful login
# session info will likely be stored on CurrentUser
# updated CurrentUser
def login(username, password):
    # create user object with username
    user = User()
    user.name = username

    #send user DTO through post
    response = session.post(url=f"{API_URL}/login/{user.to_dto}")

    # handle repsonse code (success/failure)
    # 200 okay
    # should I send error code to view for display for a popup message?
    if response.status_code != 200:
        return False

    try:
        sio.connect(API_URL)
    except ConnectionRefusedError:
        return False

    #update current user
    currentUser.add(user, session)

    return True
    """
    #https://stackoverflow.com/questions/50412530/python-multi-threading-spawning-n-concurrent-threads
    #https://stackoverflow.com/questions/15085348/what-is-the-use-of-join-in-threading
    #spawn threads for message_in and user_change
    thread = Thread(target = message_in)
    thread.start()
    thread.join()

    thread = Thread(target = user_change)
    thread.start()
    thread.join()
    """

# accepts message from server
# adds message to model
# It comes in as a DTO, right?
@sio.event
def message_in(message_dto):
    MessageList.add(Message.from_dto(message_dto))

#updating client user list to match what the server sends it
@sio.event
def user_change(user_list_dto):
    #user list remove all
    UserList.remove_all_users()

    #user list add many from dtos
    UserList.add_many_from_dtos(user_list_dto)

# sends logout POST request to server
# probably spawns a thread to handle/wait for response
# ends SocketIO connection
# sets the CurrentUser to "none" state - (to be defined)
def logout():
    response = session.post(url=f"{API_URL}/logout")

    # if post did not get to server
    if response.status_code != 200:
        #disconnect anyways?
        #perhaps server could periodically check if a user
        #is connected or not in case logout post request fails.
        pass

    # ends SocketIO connection
    sio.disconnect()

    # sets the CurrentUser to "none" state - (to be defined)
    currentUser.remove()

    return True

# sends message via SocketIO "message_out" event
def send_message(text, sender, reciever):
    #check if message is not empty
    if text != "":
        #send message to server
        sio.emit('message', Message.to_dto(Message(text, sender, reciever)))


# reconnect via websockets
def reconnect():
    try:
        sio.connect(API_URL)
        return True
    except ConnectionRefusedError:
        return False