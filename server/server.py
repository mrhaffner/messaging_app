
# login route - http POST

# logout route - http POST

# socketio "message_out" event to handle messages
# emits based on "sender/receiver" field
# "group" receiver is emitted to everyone
# otherwise the message is emitted only to the sender (for confirmation) AND receiver
# emits to "message_in" event

# socketio "user_change_out" event to handle displaying active users
# sends updated list of all logged in users whenever a user disconnects/logs in/logs out
# a user should be sent this list when they first connect?
# emits to "user_change_in" event

def main():
    pass

if __name__ == "__main__":
    main()