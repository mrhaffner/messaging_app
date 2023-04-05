import json
import pickle

from dataclasses import asdict, dataclass, field


@dataclass(unsafe_hash=True)
class User:
    name: str
    password: str = field(compare=False)
    sid: int = field(compare=False, default=None)

    def to_dto(self):
        self_dict = asdict(self)
        del self_dict['sid']
        return json.dumps(asdict(self))

    @staticmethod
    def from_dto(dto):
        user_dict = json.loads(dto)
        return User(user_dict['name'], user_dict['password'])


# code reuse ?
class UserList():

    def __init__(self):
        self._users = set()

    def add(self, user):
        if self.exists(user) or user.password is None or user.password == "":
            raise ValueError("User already exists")
        elif user.password is None or user.password == "":
            raise ValueError("Invalid Password")
        elif user.name == "" or user.name is None or user.name.lower() == "group":
            raise ValueError("Invalid Password")
        self._users.add(user)

        with open('users.pickle', 'wb') as f:
            users = UserList()
            users._users = {User(user.name, user.password) for user in self._users}
            pickle.dump(users, f)

    def add_from_dto(self, user_dto):
        self.add(User.from_dto(user_dto))

    def remove_by_username(self, username):
        for user in self._users:
            if user.name == username:
                self._users.discard(user)
                break

    def exists(self, user):
        return user in self._users

    def get_all(self):
        return list(self._users)

    def to_dto(self):
        return [user.to_dto() for user in self._users if user.sid is not None]
    
    def get_user_by_name(self, name):
        for user in self._users:
            if user.name == name:
                return user