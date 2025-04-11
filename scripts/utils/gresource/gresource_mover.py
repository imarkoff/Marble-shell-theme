import os
import shutil

from scripts.utils.logger.logger import LoggerFactory


class GresourceMover:
    def __init__(self, source_file: str, destination_file: str, logger_factory: LoggerFactory):
        self.source_file = source_file
        self.destination_file = destination_file
        self.logger_factory = logger_factory

    def move(self):
        move_line = self.logger_factory.create_logger()
        move_line.update("Moving gresource files...")

        os.makedirs(os.path.dirname(self.destination_file), exist_ok=True)
        shutil.copyfile(self.source_file, self.destination_file)
        os.chmod(self.destination_file, 0o644)

        move_line.success("Moved gresource files.")
