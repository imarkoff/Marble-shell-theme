from typing import Optional

from scripts.utils.logger.logger import LoggerFactory, Logger


class DummyLoggerFactory(LoggerFactory):
    def create_logger(self, name: Optional[str] = None) -> 'DummyLogger':
        return DummyLogger()


class DummyLogger(Logger):
    def update(self, msg):
        pass

    def success(self, msg):
        pass

    def error(self, msg):
        pass

    def warn(self, msg):
        pass

    def info(self, msg):
        pass