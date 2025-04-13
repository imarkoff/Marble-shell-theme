import os

from scripts.utils.alternatives_updater import PathString
from scripts.utils.command_runner.command_runner import CommandRunner
from scripts.utils.gresource.gresource_backuper import GresourceBackuperManager
from scripts.utils.gresource.gresource_compiler import GresourceCompiler
from scripts.utils.gresource.gresource_extractor import GresourceExtractor
from scripts.utils.gresource.gresource_mover import GresourceMover
from scripts.utils.logger.logger import LoggerFactory


class Gresource:
    """Orchestrator for gresource files."""

    def __init__(
            self, gresource_file: str, temp_folder: PathString, destination: PathString,
            logger_factory: LoggerFactory, runner: CommandRunner
    ):
        """
        :param gresource_file: The name of the gresource file to be processed.
        :param temp_folder: The temporary folder where resources will be extracted.
        :param destination: The destination folder where the compiled gresource file will be saved.
        """
        self.gresource_file = gresource_file
        self.temp_folder = temp_folder
        self.destination = destination

        self.logger_factory = logger_factory
        self.runner = runner

        self._temp_gresource = os.path.join(temp_folder, gresource_file)
        self._destination_gresource = os.path.join(destination, gresource_file)
        self._active_source_gresource = self._destination_gresource

        self._backuper = GresourceBackuperManager(self._destination_gresource,
                                                  logger_factory=self.logger_factory)

    def has_trigger(self, trigger: str) -> bool:
        """
        Check if the trigger is present in the gresource file.
        Used to detect if the theme is already installed.
        :param trigger: The trigger to check for.
        :return: True if the trigger is found, False otherwise.
        """
        return self._backuper.has_trigger(trigger)

    def use_backup_gresource(self):
        self._active_source_gresource = self._backuper.get_backup()
        return self._active_source_gresource

    def extract(self):
        extractor = GresourceExtractor(self._active_source_gresource, self.temp_folder,
                           logger_factory=self.logger_factory, runner=self.runner)
        extractor.extract()

    def compile(self):
        compiler = GresourceCompiler(self.temp_folder, self._temp_gresource,
                                     logger_factory=self.logger_factory, runner=self.runner)
        compiler.compile()

    def backup(self):
        self._backuper.backup()

    def restore(self):
        self._backuper.restore()
        self._active_source_gresource = self._destination_gresource

    def move(self):
        mover = GresourceMover(self._temp_gresource, self._destination_gresource,
                               logger_factory=self.logger_factory)
        mover.move()
