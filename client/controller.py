import requests
import socketio

from model.message import Message, MessageList
from model.user import CurrentUser, User, UserList

API_URL = "http://127.0.0.1:5000"
session = requests.Session()
sio = socketio.Client(http_session=session)
currentUser = CurrentUser()
users = UserList()
messages = MessageList()

def create_account(username, password):
    """
    Creates a user given a username and password and attempts to send it to
    the server for account creation procedure
    """
    user = User(username, password)

    try:
        response = session.post(f"{API_URL}/create_account", json=user.to_dto())
    except:
        return 503
    
    return response.status_code

def login(username, password):
    """
    Creates a user given a username and password and attempts to send it to
    the server for login procedure. If login is successful, set the clients
    current user to the one generated here
    """
    user = User(username, password)

    try:
        response = session.post(f"{API_URL}/login", json=user.to_dto())
    except:
        return 503

    if response.status_code != 200: #dont try and connect via socket if login failed
        return response.status_code

    try:
        sio.connect(API_URL)
    except:
        return response.status_code
    
    currentUser.add(user)
    return response.status_code

def logout():
    """Disconnects the socket upon logging out"""
    sio.disconnect()
    return True

@sio.on("message_out")
def message_in(message_dto):
    """Handles message DTO coming in from server"""
    messages.add(Message.from_dto(message_dto))

def send_message(text, receiver):
    """Handles sending messages to server"""
    if text != "" or receiver.name != "": #message or receiver cannot be empty
        sio.emit('message_out', Message(text, currentUser._user, receiver).to_dto())

@sio.on("user_change")
def user_change(user_list_dto):
    """Updates the user list when someone logs out or logs in"""
    users.remove_all_users()
    users.add_many_from_dtos(user_list_dto)

def kick(username):
    """Kicks a user with the specified username from the chat"""
    user = User(username)
    session.post(f"{API_URL}/kick", json=user.to_dto())


@sio.on("disconnect")
def disconnect():
    """
    Removes current user after getting disconnected from SocketIO
    Resets the session
    """
    currentUser.remove()
    messages.reset()