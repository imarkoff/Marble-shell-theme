import os
import shutil

from scripts.utils.gresource import GresourceBackupNotFoundError
from scripts.utils.logger.logger import LoggerFactory


class GresourceBackuperManager:
    def __init__(self, destination_file: str, logger_factory: LoggerFactory):
        self.destination_file = destination_file
        self._backup_file = f"{destination_file}.backup"
        self._backuper = GresourceBackuper(destination_file, self._backup_file, logger_factory)

    def has_trigger(self, trigger: str) -> bool:
        return self._backuper.has_trigger(trigger)

    def backup(self):
        self._backuper.backup()

    def restore(self):
        self._backuper.restore()

    def get_backup(self) -> str:
        return self._backuper.get_backup()


class GresourceBackuper:
    def __init__(self, destination_file: str, backup_file: str, logger_factory: LoggerFactory):
        self.destination_file = destination_file
        self.backup_file = backup_file
        self.logger_factory = logger_factory

    def has_trigger(self, trigger: str) -> bool:
        with open(self.destination_file, "rb") as f:
            return trigger.encode() in f.read()

    def get_backup(self) -> str:
        if not os.path.exists(self.backup_file):
            raise GresourceBackupNotFoundError(self.backup_file)
        return self.backup_file

    def backup(self):
        backup_line = self.logger_factory.create_logger()
        backup_line.update("Backing up gresource files...")

        if os.path.exists(self.backup_file):
            os.remove(self.backup_file)

        shutil.copy2(self.destination_file, self.backup_file)

        backup_line.success("Backed up gresource files.")

    def restore(self):
        if not os.path.exists(self.backup_file):
            raise GresourceBackupNotFoundError(self.backup_file)

        shutil.move(self.backup_file, self.destination_file)

        self.logger_factory.create_logger().success("Restored gresource files.")
