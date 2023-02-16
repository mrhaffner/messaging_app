import json
from dataclasses import asdict, dataclass

from shared import SingletonMeta


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

    users = set()

    def add(self, user):
        if self.exists(user):
            raise ValueError("User already exists")
        self.users.add(user)

    def add_from_dto(self, user_dto):
        self.add(User.from_dto(user_dto))

    # def add_many_from_dtos(self, user_dtos):
    #     for user_dto in user_dtos:
    #         self.add_from_dto(user_dto)

    def remove(self, user):
        self.users.discard(user)

    def exists(self, user):
        return user in self.users

    def get_all(self):
        return list(self.users)