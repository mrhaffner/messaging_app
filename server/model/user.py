import json
import pickle

from dataclasses import asdict, dataclass, field


@dataclass(unsafe_hash=True)
class User:
    """A user of the chat system"""
    name: str
    password: str = field(compare=False)
    sid: int = field(compare=False, default=None)  # session id, None if not logged in

    def to_dto(self):
        """Serializes this User to JSON"""
        self_dict = asdict(self)
        del self_dict["sid"]  # server info only
        return json.dumps(asdict(self))

    @staticmethod
    def from_dto(dto):
        """Creates a User from a serialized user JSON object"""
        user_dict = json.loads(dto)
        return User(user_dict["name"], user_dict["password"])


class UserList():
    """A list of all users of the chat app"""

    def __init__(self):
        """Initializes this UserList"""
        self._users = set()

    def add(self, user):
        """
        Creates a new User and saves the updated UserList to users.pickle

        Raises a ValueError if:
            The a user with that username already exists
            The password or username is empty
            The username is the reserves name "group"
        """
        if self.exists(user):
            raise ValueError("User already exists")
        elif user.password is None or user.password == "":
            raise ValueError("Invalid Password")
        elif user.name == "" or user.name is None or user.name.lower() == "group":
            raise ValueError("Invalid Username")
        self._users.add(user)

        with open("users.pickle", "wb") as f:
            # creates a duplicate list with no session ids - no Users are logged in on startup
            users = UserList()
            users._users = {User(user.name, user.password) for user in self._users}
            # save the UserList
            pickle.dump(users, f)

    def add_from_dto(self, user_dto):
        """Adds a User to this list from a user JSON object"""
        self.add(User.from_dto(user_dto))

    def exists(self, user):
        """Returns True if the user already exists, False otherwise"""
        return user in self._users

    def to_dto(self):
        """Serializes all logged in users in this UserList to a JSON array"""
        return [user.to_dto() for user in self._users if user.sid is not None]
    
    def get_user_by_name(self, name):
        """Finds a user by name. Returns None if the user is not found"""
        for user in self._users:
            if user.name == name:
                return user
        return None