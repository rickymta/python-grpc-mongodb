from dataclasses import dataclass

from app.domain.entities.LogLevel import LogLevel

@dataclass
class InnerLog:
    message: str = ""
    exception: str = ""
    stacktrace: str = ""
    level: LogLevel = LogLevel.DEBUG
