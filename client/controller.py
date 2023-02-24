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
from model.user import CurrentUser, User

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
    try:
        sio.connect(API_URL)
    except ConnectionRefusedError:
        # error popup in view?
        pass

    # create user object with username
    user = User()
    user.name = username

    #update current user
    currentUser.add(user, session)
    
    #send user DTO through post
    session.post(url=f"{API_URL}/login/{user.to_dto}")

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
    #is this all I need for this?
    MessageList.add(Message.from_dto(message_dto))

# does this mean the CurrentUser switches accounts?
# If so, this comes from the client so no DTO, right?
@sio.event
def user_change(user):
    currentUser.add(user)

# sends logout POST request to server
# probably spawns a thread to handle/wait for response
# ends SocketIO connection
# sets the CurrentUser to "none" state - (to be defined)
def logout():
    try:
        session.post(url=f"{API_URL}/logout")
    except ConnectionRefusedError:
        # error popup in view?
        pass

    # ends SocketIO connection
    sio.disconnect()

    # sets the CurrentUser to "none" state - (to be defined)
    currentUser.remove()


# sends message via SocketIO "message_out" event
@sio.event('message_out')
def send_message(id, text, sender, reciever):
    #check if message is not empty
    if text != "":
        #convert to dto here or somewhere else?
        #send message to server
        sio.emit('message', Message.to_dto(id, text, sender, reciever))


# reconnect via websockets
def reconnect():
    try:
        sio.connect(API_URL)
    except ConnectionRefusedError:
        # error popup in view?
        pass
    
# anything else needed in controller?