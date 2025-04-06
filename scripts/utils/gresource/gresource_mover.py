import subprocess

from scripts.utils.logger.logger import LoggerFactory


class GresourceMover:
    def __init__(self, source_file: str, destination_file: str, logger_factory: LoggerFactory):
        self.source_file = source_file
        self.destination_file = destination_file
        self.logger_factory = logger_factory

    def move(self):
        move_line = self.logger_factory.create_logger()
        move_line.update("Moving gresource files...")

        subprocess.run(["cp", "-f",
                        self.source_file,
                        self.destination_file],
                       check=True)

        subprocess.run(["chmod", "644", self.destination_file], check=True)

        move_line.success("Moved gresource files.")
