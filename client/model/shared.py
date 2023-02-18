class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    
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
    This is class is the Publisher in the Pub Sub pattern
    aka the Observable in the Observer pattern
    Use the subscribe() method to observe this object for changes
    Subscribers must implement the publish() method to receive updates
    """
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, subscriber):
        self._subscribers.add(subsciber)

    def publish(self):
        for subscriber in self._subscribers:
            subscriber.publish(self)