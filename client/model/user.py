import json
from dataclasses import asdict, dataclass

from .shared import Publisher, SingletonMeta


@dataclass(frozen=True)
class User:
    name: str

    def __str__(self):
        return self.name

    def to_dto(self):
        return json.dumps(asdict(self))

    @staticmethod
    def from_dto(dto):
        user_dict = json.loads(dto)
        return User(user_dict['name'])


# code reuse ?
class UserList(Publisher, metaclass=SingletonMeta):

    def __init__(self):
        super().__init__()
        self._users = set()

    def add(self, user):
        if self.exists(user):
            raise ValueError("User already exists")
        self._users.add(user)
        super().publish(self)

    def add_from_dto(self, user_dto):
        self.add(User.from_dto(user_dto))
        super().publish(self)

    def add_many_from_dtos(self, user_dtos):
        for user_dto in user_dtos:
            self.add_from_dto(user_dto)
        super().publish(self)

    def remove(self, user):
        self._users.discard(user)
        super().publish(self)

    def remove_all_users(self):
        self._users = set()
        super().publish(self)

    def exists(self, user):
        return user in self._users

    def get_all(self):
        return list(self._users)
    
    def get_by_name(self, name):
        for user in self._users:
            if user.name == name:
                return user
        return None


# represents the current user
# needs an option for when there is none
# needs to contain auth information probably
# implements observer aka pub/sub pattern with view
# is a singleton
class CurrentUser(Publisher, metaclass=SingletonMeta):

    def __init__(self):
        super().__init__()
        self._user = None
        self._session = None

    def exists(self):
        return self._user is not None

    def remove(self):
        self._user = None
        super().publish(self)

    def add(self, user, session):
        self._user = user
        self._session = session
        super().publish(self)

    @property
    def user(self):
        self._user

    @property
    def session(self):
        self._session