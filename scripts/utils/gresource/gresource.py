import os

from scripts.utils.gresource.gresource_backuper import GresourceBackuperManager
from scripts.utils.gresource.gresource_complier import GresourceCompiler
from scripts.utils.gresource.gresource_extractor import GresourceExtractor
from scripts.utils.gresource.gresource_mover import GresourceMover
from scripts.utils.logger.logger import LoggerFactory


class Gresource:
    """Orchestrator for gresource files. Manages the extraction, compilation, and backup of gresource files."""

    def __init__(self, gresource_file: str, temp_folder: str, destination: str, logger_factory: LoggerFactory):
        """
        :param gresource_file: The name of the gresource file to be processed.
        :param temp_folder: The temporary folder where resources will be extracted.
        :param destination: The destination folder where the compiled gresource file will be saved.
        """
        self.gresource_file = gresource_file
        self.temp_folder = temp_folder
        self.destination = destination
        self.logger_factory = logger_factory

        self._temp_gresource = os.path.join(temp_folder, gresource_file)
        self._destination_gresource = os.path.join(destination, gresource_file)
        self._active_source_gresource = self._destination_gresource

        self._backuper = GresourceBackuperManager(self._destination_gresource, logger_factory=self.logger_factory)

    def use_backup_gresource(self):
        self._active_source_gresource = self._backuper.get_backup()

    def extract(self):
        GresourceExtractor(self._active_source_gresource, self.temp_folder, logger_factory=self.logger_factory).extract()

    def compile(self):
        GresourceCompiler(self.temp_folder, self._temp_gresource, logger_factory=self.logger_factory).compile()

    def backup(self):
        self._backuper.backup()

    def restore(self):
        self._backuper.restore()

    def move(self):
        GresourceMover(self._temp_gresource, self._destination_gresource, logger_factory=self.logger_factory).move()
