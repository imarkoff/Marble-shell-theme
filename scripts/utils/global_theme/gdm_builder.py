import os.path
from typing import Optional

from scripts import config
from scripts.install.colors_definer import ColorsDefiner
from scripts.types.installation_color import InstallationMode
from scripts.utils.alternatives_updater import AlternativesUpdater, PathString
from scripts.utils.command_runner.subprocess_command_runner import SubprocessCommandRunner
from scripts.utils.files_labeler import FilesLabelerFactoryImpl
from scripts.utils.global_theme.gdm import GDMTheme
from scripts.utils.global_theme.gdm_installer import GDMThemeInstaller
from scripts.utils.global_theme.gdm_preparer import GDMThemePreparer
from scripts.utils.global_theme.gdm_remover import GDMThemeRemover
from scripts.utils.global_theme.ubuntu_alternatives_updater import UbuntuGDMAlternativesUpdater
from scripts.utils.gresource.gresource import Gresource
from scripts.utils.logger.console import Console
from scripts.utils.logger.logger import LoggerFactory
from scripts.utils.theme.gnome_shell_theme_builder import GnomeShellThemeBuilder


class GDMThemeBuilder:
    """
    Builder class for creating GDMTheme instances with configurable components.

    This class follows the Builder pattern to create a GDMTheme with all necessary
    dependencies. Dependencies can be injected via the with_* methods or will be
    automatically resolved during build() if not provided.

    Example usage:
        builder = GMDThemeBuilder(colors_provider)
        theme = builder.with_mode("dark").with_filled(True).build()
    """
    def __init__(self, colors_provider: ColorsDefiner):
        """
        :param colors_provider: A provider for color definitions.
        """
        self.colors_provider: ColorsDefiner = colors_provider
        self._temp_folder: PathString = os.path.join(config.temp_folder, config.gdm_folder)
        self._mode: Optional[InstallationMode] = None
        self._is_filled: bool = False

        self._logger_factory: Optional[LoggerFactory] = None
        self._gresource: Optional[Gresource] = None
        self._ubuntu_gdm_alternatives_updater: Optional[UbuntuGDMAlternativesUpdater] = None

        self._preparer: Optional[GDMThemePreparer] = None
        self._installer: Optional[GDMThemeInstaller] = None
        self._remover: Optional[GDMThemeRemover] = None

    def with_mode(self, mode: InstallationMode | None) -> 'GDMThemeBuilder':
        """Set the mode for the theme."""
        self._mode = mode
        return self

    def with_filled(self, is_filled=True) -> 'GDMThemeBuilder':
        """Set the filled state for the theme."""
        self._is_filled = is_filled
        return self

    def with_logger_factory(self, logger_factory: LoggerFactory) -> 'GDMThemeBuilder':
        """Inject a logger factory for logging purposes."""
        self._logger_factory = logger_factory
        return self

    def with_gresource(self, gresource: Gresource) -> 'GDMThemeBuilder':
        """Inject a gresource instance for managing gresource files."""
        self._gresource = gresource
        return self

    def with_ubuntu_gdm_alternatives_updater(self, alternatives_updater: UbuntuGDMAlternativesUpdater) -> 'GDMThemeBuilder':
        """Inject an alternatives updater for managing GDM alternatives."""
        self._ubuntu_gdm_alternatives_updater = alternatives_updater
        return self

    def with_preparer(self, preparer: GDMThemePreparer) -> 'GDMThemeBuilder':
        """Inject a preparer for preparing the theme."""
        self._preparer = preparer
        return self

    def with_installer(self, installer: GDMThemeInstaller) -> 'GDMThemeBuilder':
        """Inject an installer for installing the theme."""
        self._installer = installer
        return self

    def with_remover(self, remover: GDMThemeRemover) -> 'GDMThemeBuilder':
        """Inject a remover for removing the theme."""
        self._remover = remover
        return self

    def build(self) -> GDMTheme:
        """
        Build the GDMTheme object with the configured components.

        Automatically resolves any dependencies that haven't been explicitly
        provided through with_* methods. The order of resolution ensures
        that dependencies are created before they're needed.

        :return: A fully configured GDMTheme instance ready for use
        """
        self._resolve_logger_factory()
        self._resolve_gresource()
        self._resolve_ubuntu_gdm_alternatives_updater()

        self._resolve_preparer()
        self._resolve_installer()
        self._resolve_remover()

        return GDMTheme(self._preparer, self._installer, self._remover)

    def _resolve_logger_factory(self):
        """Instantiate a default Console logger if not explicitly provided."""
        if self._logger_factory: return
        self._logger_factory = Console()

    def _resolve_gresource(self):
        """
        Create a Gresource handler if not explicitly provided.
        Uses configuration values for file paths and destinations.
        """
        if self._gresource: return

        gresource_file = config.gnome_shell_gresource
        temp_folder = os.path.join(self._temp_folder, config.extracted_gdm_folder)
        destination = config.global_gnome_shell_theme
        runner = SubprocessCommandRunner()

        self._gresource = Gresource(
            gresource_file=gresource_file,
            temp_folder=temp_folder,
            destination=destination,
            logger_factory=self._logger_factory,
            runner=runner
        )

    def _resolve_ubuntu_gdm_alternatives_updater(self):
        """Create an UbuntuGDMAlternativesUpdater if not explicitly provided."""
        if self._ubuntu_gdm_alternatives_updater: return
        alternatives_updater = AlternativesUpdater()
        self._ubuntu_gdm_alternatives_updater = UbuntuGDMAlternativesUpdater(alternatives_updater)

    def _resolve_preparer(self):
        """Create a GDMThemePreparer if not explicitly provided."""
        if self._preparer: return
        theme_builder = GnomeShellThemeBuilder(self.colors_provider)
        files_labeler_factory = FilesLabelerFactoryImpl()
        self._preparer = GDMThemePreparer(
            temp_folder=self._temp_folder,
            default_mode=self._mode,
            is_filled=self._is_filled,
            gresource=self._gresource,
            theme_builder=theme_builder,
            logger_factory=self._logger_factory,
            files_labeler_factory=files_labeler_factory,
        )

    def _resolve_installer(self):
        """Create a GDMThemeInstaller if not explicitly provided."""
        if self._installer: return
        self._installer = GDMThemeInstaller(
            gresource=self._gresource,
            alternatives_updater=self._ubuntu_gdm_alternatives_updater,
        )

    def _resolve_remover(self):
        """Create a GDMThemeRemover if not explicitly provided."""
        if self._remover: return
        self._remover = GDMThemeRemover(
            gresource=self._gresource,
            alternatives_updater=self._ubuntu_gdm_alternatives_updater,
            logger_factory=self._logger_factory
        )