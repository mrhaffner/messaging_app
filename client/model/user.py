# for communicating with the server
class UserDTO:
    pass

# represenets other Users
class User:
    pass


# represents the current user
# needs an option for when there is none
# needs to contain auth information probably
# implements observer aka pub/sub pattern with view
# is a singleton
class CurrentUser:
    pass


# singleton list of all other users online
# implements observer aka pub/sub pattern with view
class UserList:
    pass