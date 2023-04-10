import json

from dataclasses import asdict, dataclass, field

from .shared import Publisher, SingletonMeta
from .user import User


@dataclass()
class Message:
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
        return Message(message_dict['text'], 
                       User(message_dict['sender']['name']), 
                       User(message_dict['receiver']['name']), 
                       message_dict['type'])


class MessageList(Publisher, metaclass=SingletonMeta):
    """A list of all received/sent messages"""

    def __init__(self):
        """Initializes this MessageList"""
        super().__init__()
        self._messages = []

    def add(self, message):
        """Add a Mesage to this List"""
        self._messages.append(message)
        super().publish(self)  # lets the view know there is an update

    def _add_from_dto(self, message_dto):
        """Adds a Message to this list from a message JSON object"""
        self._messages.append(Message.from_dto(message_dto))

    def add_many_from_dtos(self, messages_dto):
        """Adds a messages to this list from a list of message JSON objects"""
        for message_dto in messages_dto:
            self._add_from_dto(message_dto)
        super().publish(self)  # lets the view know there is an update

    def get_all(self):
        """Returns a list of all Messages"""
        return self._messages
    
    def reset(self):
        """Removes all Messages from the list"""
        self._messages = []
        super().publish(self)  # lets the view know there is an update