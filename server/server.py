
# login route - http POST

# logout route - http POST

# socketio "message" event to handle messages
# emits based on "sender/receiver" field
# "group" receiver is emitted to everyone
# otherwise the message is emitted only to the sender (for confirmation) AND receiver

# socketio "user_change" event to handle displaying active users
# sends updated list of all logged in users whenever a user disconnects/logs in/logs out
# a user should be sent this list when they first connect?

def main():
    pass

if __name__ == "__main__":
    main()