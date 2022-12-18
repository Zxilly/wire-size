from abc import ABC
from click import Command


class Provider(ABC):
    @staticmethod
    def command() -> Command:
        pass
