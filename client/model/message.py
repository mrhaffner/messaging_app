# used for sharing data with server
class MessageDTO:
    pass


# needs an attribute to indicate if send failed/waiting for response
class Message:
    pass

# singleton list of all messages received
# implements observer aka pub/sub pattern with view
class MessageList:
    pass