import re
import time
from abc import abstractmethod, ABCMeta

from app.database import Database


class Utils:
    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        return True if email_address_matcher.match(email) else False

    @staticmethod
    def timestamp():
        """Return the current timestamp as an integer."""
        return int(time.time())


class Savable(metaclass=ABCMeta):
    def save(self):
        Database.insert(self.to_dict())

    @abstractmethod
    def to_dict(self):
        pass
