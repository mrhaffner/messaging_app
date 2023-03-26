import json
from dataclasses import asdict, dataclass, field

from .user import User


class UniqueId:

    next_id = 1

    @staticmethod
    def get_id():
        new_id = UniqueId.next_id
        UniqueId.next_id += 1
        return new_id


@dataclass()
class Message:
    id: int = field(init=False)
    text: str = field(compare=False)
    sender: User = field(compare=False)
    receiver: User = field(compare=False)

    def __post_init__(self):
        self.id = UniqueId.get_id()

    def to_dto(self):
        return json.dumps(asdict(self))

    @staticmethod
    def from_dto(dto):
        message_dict = json.loads(dto)
        return Message(
                        message_dict['text'], 
                        User.from_dto(json.dumps(message_dict['sender'])),  # necessary?
                        User.from_dto(json.dumps(message_dict['receiver']))  # necessary?
                      )


