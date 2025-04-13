from scripts.types.theme_base import ThemeBase
from scripts.utils.global_theme.gdm_installer import GDMThemeInstaller
from scripts.utils.global_theme.gdm_preparer import GDMThemePreparer
from scripts.utils.global_theme.gdm_remover import GDMThemeRemover
from scripts.utils.global_theme.gdm_theme_prepare import GDMThemePrepare


class GDMTheme(ThemeBase):
    """
    GDM theming module.

    This module provides functionality to prepare, install, and remove GNOME Display Manager themes.
    It follows a workflow of:
    1. Preparing themes from existing GDM resources
    2. Installing themes with custom colors/styles
    3. Providing ability to restore original GDM themes

    The main entry point is the GDMTheme class, which orchestrates the entire theme management process.
    """
    def __init__(self, preparer: GDMThemePreparer, installer: GDMThemeInstaller, remover: GDMThemeRemover):
        """
        :param preparer: GDMThemePreparer instance for preparing themes
        :param installer: GDMThemeInstaller instance for installing themes
        :param remover: GDMThemeRemover instance for removing themes
        """
        self.preparer = preparer
        self.installer = installer
        self.remover = remover

        self.themes: list[GDMThemePrepare] = []

    def prepare(self):
        """
        Prepare the theme for installation.

        This method:
        1. Checks if a theme is already installed and uses backup if needed
        2. Extracts relevant theme files
        3. Processes them into ready-to-compile GDMThemePrepare objects

        The processed themes are stored in the themes attribute for later use.
        """
        if self._is_installed():
            self.preparer.use_backup_as_source()
        self.themes = self.preparer.prepare()

    def _is_installed(self) -> bool:
        """
        Check if a GDM theme is currently installed.

        This looks for specific markers in the system gresource files
        that indicate our theme has been installed.

        :return: True if a custom theme is installed, False otherwise
        """
        return self.installer.is_installed()

    def install(self, hue: int, name: str, sat: float | None = None):
        """
        Install the prepared theme with specified color adjustments.

        This method:
        1. Compiles theme files with the specified hue and saturation
        2. Creates a backup of the original GDM theme if one doesn't exist
        3. Installs the compiled theme to the system

        :param hue: The hue adjustment (0-360) to apply to the theme
        :param name: The name of the theme to be installed. In GDM will only be shown in logger
        :param sat: Optional saturation adjustment (0-100) to apply
        """
        self.installer.compile(self.themes, hue, name, sat)

        if not self._is_installed():
            self.installer.backup()

        self.installer.install()

    def remove(self):
        """
        Remove the installed theme and restore the original GDM theme.

        If no theme is installed, displays a warning message to the user.
        This will restore from backup and update GDM alternatives if needed.
        """
        if self._is_installed():
            self.remover.remove()
        else:
            self.remover.warn_not_installed()
