import json
from dataclasses import asdict, dataclass

from shared import SingletonMeta
from user import User


@dataclass(frozen=True)
class Message:
    id: int = field(init=False, default=Message.get_unique_id())
    text: str = field(compare=False)
    sender: User = field(compare=False)
    receiver: User = field(compare=False)

    next_id = 1

    def to_dto(self):
        return json.dumps(asdict(self)) # works with User?

    @staticmethod
    def get_unique_id():
        new_id = Message.next_id
        Message.next_id += 1
        return new_id

    @staticmethod
    def from_dto(dto):
        message_dict = json.loads(dto)
        return Message(
                        message_dict['text'], 
                        User.from_dto(message_dict['sender']),  # necessary?
                        User.from_dto(message_dict['receiver'])  # necessary?
                      )