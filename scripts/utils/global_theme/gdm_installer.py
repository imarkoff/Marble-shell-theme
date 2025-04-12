from scripts.utils.global_theme.gdm_theme_prepare import GDMThemePrepare
from scripts.utils.global_theme.ubuntu_alternatives_updater import UbuntuGDMAlternativesUpdater
from scripts.utils.gresource.gresource import Gresource


class GDMThemeInstaller:
    """
    Handles the installation of GDM themes system-wide.

    This class manages:
    - Compiling prepared theme resources into a gresource file
    - Creating backups of original system files
    - Installing compiled themes via the alternatives system
    - Detecting if a theme is already installed
    """
    def __init__(self, gresource: Gresource, alternatives_updater: UbuntuGDMAlternativesUpdater):
        """
        :param gresource: Handler for gresource operations
        :param alternatives_updater: Handler for update-alternatives operations
        """
        self.gresource = gresource
        self.alternatives_updater = alternatives_updater

        self._is_installed_trigger = "\n/* Marble theme */\n"

    def is_installed(self) -> bool:
        """
        Check if the theme is installed
        by looking for the trigger in the gresource file.
        """
        return self.gresource.has_trigger(self._is_installed_trigger)

    def compile(self, themes: list[GDMThemePrepare], hue: int, color: str, sat: int = None):
        """
        Prepares themes for gresource and compiles them.
        :param themes: themes to be compiled
        :param hue: hue value for the theme
        :param color: the color name. in GDM will only be shown in logger
        :param sat: saturation value for the theme
        """
        self._generate_themes(themes, hue, color, sat)
        self.gresource.compile()

    def _generate_themes(self, themes: list[GDMThemePrepare], hue: int, color: str, sat: int = None):
        """Generate theme files for further compiling by gresource"""
        for theme_prepare in themes:
            if theme_prepare.label is not None:
                theme_prepare.label_theme()

            theme_prepare.remove_keywords("!important")
            theme_prepare.remove_properties("background-color", "color", "box-shadow", "border-radius")
            theme_prepare.prepend_source_styles(self._is_installed_trigger)

            theme_prepare.install(hue, color, sat, destination=self.gresource.temp_folder)

    def backup(self):
        """Backup the current gresource file."""
        self.gresource.backup()

    def install(self):
        """
        Install the theme globally by moving the compiled gresource file to the destination.
        Also updates the alternatives for the gdm theme.
        """
        self.gresource.move()
        self.alternatives_updater.install_and_set()