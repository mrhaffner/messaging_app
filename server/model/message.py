import json
from dataclasses import asdict, dataclass, field

from .user import User


@dataclass()
class Message:
    """A message between users"""
    text: str = field(compare=False)
    sender: User = field(compare=False)
    receiver: User = field(compare=False)
    type: str = field(compare=False, default=None)  # if this is a group message

    def to_dto(self):
        """Serializes this Message to JSON"""
        return json.dumps(asdict(self))

    @staticmethod
    def from_dto(dto):
        """Creates a Message from a serialized message JSON object"""
        message_dict = json.loads(dto)
        return Message(
                        message_dict["text"], 
                        User.from_dto(json.dumps(message_dict["sender"])),
                        User.from_dto(json.dumps(message_dict["receiver"])),
                      )