import os.path

from scripts import config
from scripts.install.colors_definer import ColorsDefiner
from scripts.utils.color_converter.color_converter_impl import ColorConverterImpl
from scripts.utils.logger.console import Console
from scripts.utils.logger.logger import LoggerFactory
from scripts.utils.style_manager import StyleManager
from scripts.utils.theme.theme import Theme
from scripts.utils.theme.theme_color_applier import ThemeColorApplier
from scripts.utils.theme.color_replacement_generator import ColorReplacementGenerator
from scripts.utils.theme.theme_installer import ThemeInstaller
from scripts.utils.theme.theme_path_provider import ThemePathProvider
from scripts.utils.theme.theme_preparation import ThemePreparation
from scripts.utils.theme.theme_temp_manager import ThemeTempManager
from theme import SourceFolder


class GnomeShellThemeBuilder:
    """
    Builder for creating a Gnome Shell theme.

    Example:
        builder = GnomeShellThemeBuilder(colors_provider)
        theme = builder.with_mode("dark").filled().build()
        theme.prepare()
        theme.install(hue=200, name="MyTheme")
    """

    def __init__(self, colors_provider: ColorsDefiner):
        self.theme_name = "gnome-shell"
        self.colors_provider = colors_provider
        self.source_folder = SourceFolder().gnome_shell
        self._base_temp_folder = config.temp_folder
        self.destination_folder = config.themes_folder
        self.mode = None
        self.is_filled = False

        self.temp_folder = os.path.join(self._base_temp_folder, self.theme_name)
        self.main_styles = os.path.join(self.temp_folder, f"{self.theme_name}.css")

        self.logger_factory: LoggerFactory | None = None
        self.preparation: ThemePreparation | None = None
        self.installer: ThemeInstaller | None = None

    def __update_paths(self):
        """Update derived paths when base folder or theme name changes"""
        self.temp_folder = os.path.join(self._base_temp_folder, self.theme_name)
        self.main_styles = os.path.join(self.temp_folder, f"{self.theme_name}.css")

    def with_temp_folder(self, temp_folder: str):
        """Set the base temporary folder"""
        self._base_temp_folder = temp_folder
        self.__update_paths()
        return self

    def with_theme_name(self, theme_name: str):
        """Set the theme name"""
        self.theme_name = theme_name
        self.__update_paths()
        return self

    def with_mode(self, mode):
        self.mode = mode
        return self

    def filled(self, filled = True):
        self.is_filled = filled
        return self

    def with_logger_factory(self, logger_factory: LoggerFactory | None):
        """Inject a logger factory for logging purposes."""
        self.logger_factory = logger_factory
        return self

    def with_preparation(self, preparation: ThemePreparation | None):
        """Inject a preparation instance for preparing the theme."""
        self.preparation = preparation
        return self

    def with_installer(self, installer: ThemeInstaller | None):
        """Inject an installer for installing the theme."""
        self.installer = installer
        return self


    def with_reset_dependencies(self):
        """Reset the dependencies for the theme preparation and installation."""
        self.preparation = None
        self.installer = None
        return self

    def build(self) -> "Theme":
        """
        Constructs and returns a Theme instance using the configured properties.

        This method resolves all necessary dependencies for the theme's preparation
        and installation. The returned Theme will have the mode and filled options set
        according to the builder's configuration.

        :return: Theme instance ready for preparation and installation
        """
        self._resolve_preparation()
        self._resolve_installer()
        return Theme(self.preparation, self.installer, self.mode, self.is_filled)

    def _resolve_preparation(self):
        if self.preparation: return

        file_manager = ThemeTempManager(self.temp_folder)
        style_manager = StyleManager(self.main_styles)
        self.preparation = ThemePreparation(self.source_folder,
                                            file_manager=file_manager, style_manager=style_manager)

    def _resolve_installer(self):
        if self.installer: return

        color_converter = ColorConverterImpl()
        color_replacement_generator = ColorReplacementGenerator(
            colors_provider=self.colors_provider,
            color_converter=color_converter)
        color_applier = ThemeColorApplier(color_replacement_generator=color_replacement_generator)
        logger_factory = self.logger_factory or Console()
        path_provider = ThemePathProvider()
        self.installer = ThemeInstaller(self.theme_name, self.temp_folder, self.destination_folder,
                                        logger_factory=logger_factory,
                                        color_applier=color_applier,
                                        path_provider=path_provider)