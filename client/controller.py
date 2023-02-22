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

#how to get user.py in controller
#import model

API_URL = "http://127.0.0.1:5000"
session = requests.Session()
sio = socketio.Client(http_session=session)

# sends login POST request to server
# probably spawns a thread to handle/wait for response
# connects via SocketIO after succesful login
# session info will likely be stored on CurrentUser
# updated CurrentUser
def login(self, username, password):
    response = session.get(url=API_URL)
    # if response is x, login view with error

    response = session.post(url=f"{API_URL}/login/{username, password}")
    # if response is x, login view with error

    sio.connect(API_URL)
    #could use try/catch for the above

    #update current user

    #https://stackoverflow.com/questions/50412530/python-multi-threading-spawning-n-concurrent-threads
    #https://stackoverflow.com/questions/15085348/what-is-the-use-of-join-in-threading
    #spawn threads for message_in and user_change
    thread = Thread(target = message_in)
    thread.start()
    thread.join()

    thread = Thread(target = user_change)
    thread.start()
    thread.join()

@sio.event
def message_in():
    pass

@sio.event
def user_change():
    pass

# sends logout POST request to server
# probably spawns a thread to handle/wait for response
# ends SocketIO connection
# sets the CurrentUser to "none" state - (to be defined)
def logout(self):
    response = session.post(url=f"{API_URL}/logout")
    #if response ix X, logout failed?

    sio.disconnect()

    #update current user


# sends message via SocketIO "message_out" event
@sio.event('message_out')
def send_message(self, message):
    #check if message is not empty
    if message != "":
        #send message to server
        sio.emit('message', message)

        #should message be sent to model as well, or should it be only sent to server and then
        #sent back to clients model?


# reconnect via websockets
def reconnect(self):
    sio.connect(API_URL)
