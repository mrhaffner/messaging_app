class SingletonMeta(type):
    """
    Only one instance of this class may exists at a time. 
    
    Source: https://refactoring.guru/design-patterns/singleton/python/example
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Publisher:
    """
    A Publisher notifies any of its subscribers when the publish event is called.
    For the Pub/Sub aka Observer design pattern.
    """
    def __init__(self):
        """Initializes this Publisher"""
        self._subscribers = set()  # all objects subscribed to this Publisher

    def subscribe(self, subscriber):
        """Subscribes to this Publisher"""
        self._subscribers.add(subscriber)

    def publish(self, obj):
        """Notifies all subscribers"""
        for subscriber in self._subscribers:
            subscriber.publish(obj)
