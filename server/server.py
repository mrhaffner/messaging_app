
# login route - http POST
# create a user session which will allow one to connect via websockets

# logout route - http POST
# emits to "user_change" event
# maybe ends the user session?

# socketio "message_out" event to handle messages
# emits based on "sender/receiver" field
# "group" receiver is emitted to everyone
# otherwise the message is emitted only to the sender (for confirmation) AND receiver
# emits to "message_in" event

# needs to handle when a user disconnects from SocketIO (seperate from logout)
# emits to "user_change" event

# needs to handle when a user first connects via SocketIO
# emits to "user_change" event but ONLY for that user
# cannot connect if does not have a session gained from login route

def main():
    pass

if __name__ == "__main__":
    main()