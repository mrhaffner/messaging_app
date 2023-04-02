import json

from dataclasses import asdict, dataclass, field

from .shared import Publisher, SingletonMeta
from .user import User


@dataclass()
class Message:
    text: str = field(compare=False)
    sender: User = field(compare=False)
    receiver: User = field(compare=False)
    id: int = field(default=None) # default for user created
    type: str = field(compare=False, default=None)

    def to_dto(self):
        return json.dumps(asdict(self)) # works with User? # remove id since it won't have one

    @staticmethod
    def from_dto(dto):
        message_dict = json.loads(dto)
        return Message(message_dict['text'], 
                       User(message_dict['sender']['name']), 
                       User(message_dict['receiver']['name']), 
                       message_dict['id'],
                       message_dict['type']
                       )


# singleton list of all messages received
# implements observer aka pub/sub pattern with view
class MessageList(Publisher, metaclass=SingletonMeta):

    def __init__(self):
        super().__init__()
        self._messages = []

    def add(self, message):
        self._messages.append(message)
        super().publish(self)

    def add_from_dto(self, message_dto):
        self.add(Message.from_dto(message_dto))
        super().publish(self)

    def add_many_from_dtos(self, messages_dto):
        for message_dto in messages_dto:
            self.add_from_dto(message_dto)
        super().publish(self)

    def remove(self, message):
        self._messages.discard(message)
        super().publish(self)

    def get_all(self):
        return self._messages