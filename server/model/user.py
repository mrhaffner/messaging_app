import json

from dataclasses import asdict, dataclass

from .shared import SingletonMeta


@dataclass(frozen=True)
class User:
    name: str

    def to_dto(self):
        return json.dumps(asdict(self))

    @staticmethod
    def from_dto(dto):
        user_dict = json.loads(dto)
        return User(user_dict['name'])


# code reuse ?
class UserList(metaclass=SingletonMeta):

    def __init__(self):
        self._users = set()

    def add(self, user):
        if self.exists(user):
            raise ValueError("User already exists")
        self._users.add(user)

    def add_from_dto(self, user_dto):
        self.add(User.from_dto(user_dto))

    def remove_by_username(self, username):
        self._users.discard(User(username))

    def exists(self, user):
        return user in self._users

    def get_all(self):
        return list(self._users)

    def to_dto(self):
        return [user.to_dto() for user in self._users]