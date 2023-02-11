# Updates the model based on button presses, POST results and incoming socketio events
# may need to wait for responses from server for some of the updates
# buttons will general call a method from the controller
# threading may be an issue when communicating with the server
# is a singleton
class ChatController:
    # this controller probably needs to spawn a thread to handle
    # listening for the following SocketIO events (see prototype for examples):
    #   "message_in" :
    #       adds message to MessageList (or updates a sent message to success/fail)
    #   "user_change" :
    #       updates the UserList
    # this should probably be done after a succesful login
    # thread is killed on disconnected/logout


    # sends login POST request to server
    # probably spawns a thread to handle/wait for response
    # connects via SocketIO after succesful login
    # session info will likely be stored on CurrentUser
    # updated CurrentUser
    def login(self):
        pass

    # sends logout POST request to server
    # probably spawns a thread to handle/wait for response
    # ends SocketIO connection
    # sets the CurrentUser to "none" state - (to be defined)
    def logout(self):
        pass

    # sends message via SocketIO "message_out" event
    def send_message(self):
        pass

    # reconnect via websockets
    def reconnect(self):
        pass