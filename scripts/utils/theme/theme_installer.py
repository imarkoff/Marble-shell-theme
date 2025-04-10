from scripts.types.installation_color import InstallationColor, InstallationMode
from scripts.utils import copy_files
from scripts.utils.logger.console import Console, Color, Format
from scripts.utils.logger.logger import LoggerFactory
from scripts.utils.theme.theme_color_applier import ThemeColorApplier
from scripts.utils.theme.theme_path_provider import ThemePathProvider


class ThemeInstaller:
    """
    Handles the installation of themes by copying files and applying color schemes.
    """

    def __init__(self, theme_type: str, source_folder: str, destination_folder: str,
                 logger_factory: LoggerFactory, color_applier: ThemeColorApplier, path_provider: ThemePathProvider):
        """
        :param theme_type: type of the theme (e.g., gnome-shell, gtk)
        :param source_folder: folder containing the theme files (e.g. temp folder)
        :param destination_folder: folder where the theme will be installed
        """
        self.theme_type = theme_type
        self.source_folder = source_folder
        self.destination_folder = destination_folder

        self.logger_factory = logger_factory
        self.color_applier = color_applier
        self.path_provider = path_provider

    def install(self, theme_color: InstallationColor, name: str, custom_destination: str = None):
        """
        Install theme and generate theme with specified accent color
        :param theme_color: object containing color and modes
        :param name: theme name
        :param custom_destination: optional custom destination folder
        """
        logger = InstallationLogger(name, theme_color.modes, self.logger_factory)

        try:
            self._perform_installation(theme_color, name, custom_destination=custom_destination)
            logger.success()
        except Exception as err:
            logger.error(str(err))
            raise

    def _perform_installation(self, theme_color, name, custom_destination=None):
        for mode in theme_color.modes:
            destination = (custom_destination or
                    self.path_provider.get_theme_path(
                        self.destination_folder, name, mode, self.theme_type))

            copy_files(self.source_folder, destination)
            self.color_applier.apply(theme_color, destination, mode)


class InstallationLogger:
    def __init__(self, name: str, modes: list[InstallationMode], logger_factory: LoggerFactory):
        self.name = name
        self.modes = modes

        self.logger = logger_factory.create_logger(self.name)
        self._setup_logger()

    def _setup_logger(self):
        self.formatted_name = Console.format(self.name.capitalize(),
                                        color=Color.get(self.name),
                                        format_type=Format.BOLD)
        joint_modes = f"({', '.join(self.modes)})"
        self.formatted_modes = Console.format(joint_modes, color=Color.GRAY)
        self.logger.update(f"Creating {self.formatted_name} {self.formatted_modes} theme...")

    def success(self):
        self.logger.success(f"{self.formatted_name} {self.formatted_modes} theme created successfully.")

    def error(self, error_message: str):
        self.logger.error(f"Error installing {self.formatted_name} theme: {error_message}")