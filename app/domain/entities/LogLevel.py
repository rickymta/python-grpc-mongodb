from enum import Enum

class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    FATAL = 4
    CRITICAL = 5

    @classmethod
    def is_valid(cls, value):
        return value in cls.__members__
