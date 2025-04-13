from abc import ABC, abstractmethod
from typing import Optional


class LoggerFactory(ABC):
    @staticmethod
    @abstractmethod
    def create_logger(name: Optional[str] = None) -> 'Logger':
        """
        Create a logger instance with the given name.
        :param name: Name of the logger.
        :return: Logger instance.
        """
        pass


class Logger(ABC):
    @abstractmethod
    def update(self, message: str):
        pass

    @abstractmethod
    def success(self, message):
        pass

    @abstractmethod
    def error(self, message):
        pass

    @abstractmethod
    def warn(self, message):
        pass

    @abstractmethod
    def info(self, message):
        pass