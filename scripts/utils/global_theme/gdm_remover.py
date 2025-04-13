from scripts.utils.global_theme.ubuntu_alternatives_updater import UbuntuGDMAlternativesUpdater
from scripts.utils.gresource import GresourceBackupNotFoundError
from scripts.utils.gresource.gresource import Gresource
from scripts.utils.logger.console import Console, Color, Format
from scripts.utils.logger.logger import LoggerFactory


class GDMThemeRemover:
    """
    Responsible for safely removing installed GDM themes.

    This class handles:
    - Restoring original gresource files from backups
    - Removing theme alternatives from the system
    - Providing feedback about removal status
    """
    def __init__(self,
                 gresource: Gresource,
                 alternatives_updater: UbuntuGDMAlternativesUpdater,
                 logger_factory: LoggerFactory):
        """
        :param gresource: Handler for gresource operations
        :param alternatives_updater: Handler for update-alternatives operations
        :param logger_factory: Factory for creating loggers
        """
        self.gresource = gresource
        self.alternatives_updater = alternatives_updater
        self.remover_logger = GDMRemoverLogger(logger_factory)

    def remove(self):
        """Restores the gresource backup and removes the alternatives."""
        self.remover_logger.start_removing()

        try:
            self.gresource.restore()
            self.alternatives_updater.remove()
            self.remover_logger.success_removing()
        except GresourceBackupNotFoundError:
            self.remover_logger.error_removing()

    def warn_not_installed(self):
        self.remover_logger.not_installed_warning()


class GDMRemoverLogger:
    def __init__(self, logger_factory: LoggerFactory):
        self.logger_factory = logger_factory
        self.removing_line = None

    def start_removing(self):
        self.removing_line = self.logger_factory.create_logger()
        self.removing_line.update("Theme is installed. Removing...")

    def success_removing(self):
        self.removing_line.success("Global theme removed successfully. Restart GDM to apply changes.")

    def error_removing(self):
        formatted_shell = Console.format("gnome-shell", color=Color.BLUE, format_type=Format.BOLD)
        self.removing_line.error(f"Backup file not found. Try reinstalling {formatted_shell} package.")

    def not_installed_warning(self):
        self.logger_factory.create_logger().error(
            "Theme is not installed. Nothing to remove.")
        self.logger_factory.create_logger().warn(
            "If theme is still installed globally, try reinstalling gnome-shell package.")