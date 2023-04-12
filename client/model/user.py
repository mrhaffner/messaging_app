import json

from dataclasses import asdict, dataclass

from .shared import Publisher, SingletonMeta


@dataclass(frozen=True)
class User:
    """A user of the chat system"""
    name: str
    password: str = None

    def to_dto(self):
        """Serializes this User to JSON"""
        return json.dumps(asdict(self))

    @staticmethod
    def from_dto(dto):
        """Creates a User from a serialized user JSON object"""
        user_dict = json.loads(dto)
        return User(user_dict["name"], user_dict["password"])


class UserList(Publisher, metaclass=SingletonMeta):
    """A list of all other users logged in to the chat app"""

    def __init__(self):
        """Initializes this UserList"""
        super().__init__()
        self.current_user = None  # keeps track of the current user
        self._users = set()  # keeps track of all other users

    def _add(self, user):
        """Adds a users to this list"""
        if user != self.current_user:
            # do not add the currently logged in user
            self._users.add(user)

    def _add_from_dto(self, user_dto):
        """Adds a User to this list from a user JSON object"""
        self._add(User.from_dto(user_dto))

    def add_many_from_dtos(self, user_dtos):
        """Adds a users to this list from a list of user JSON objects"""
        for user_dto in user_dtos:
            self._add_from_dto(user_dto)
        super().publish(self)  # lets the view know there is an update

    def remove_all_users(self):
        """Clears the user list"""
        self._users = set()
        super().publish(self)  # lets the view know there is an update

    def get_all(self):
        """Returns a list of all currently logged in Users"""
        return list(self._users)
    
    def get_by_name(self, name):
        """Finds a user by name. Returns None if the user is not found"""
        for user in self._users:
            if user.name == name:
                return user
        return None


class CurrentUser(Publisher, metaclass=SingletonMeta):
    """The currently logged in user of this chat app"""

    def __init__(self):
        """Initializes this CurrentUser"""
        super().__init__()
        self._user = None  # None indicates there is no user logged in

    def exists(self):
        """Returns whether there is a currently logged in user or not"""
        return self._user is not None

    def remove(self):
        """Sets the current user to None"""
        self._user = None
        super().publish(self)  # lets the view know there is an update

    def add(self, user):
        """Adds a CurrentUser"""
        self._user = user
        super().publish(self)  # lets the view know there is an update