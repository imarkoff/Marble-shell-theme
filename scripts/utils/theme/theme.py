from scripts.types.installation_color import InstallationColor
from scripts.types.theme_base import ThemeBase
from scripts.utils.theme.theme_installer import ThemeInstaller
from scripts.utils.theme.theme_preparation import ThemePreparation


class Theme(ThemeBase):
    """
    Manages theme preparation and installation.

    The Theme class orchestrates the process of preparing a theme by combining files,
    applying color schemes, and installing the final theme into a destination folder.
    """

    def __init__(self, preparation: ThemePreparation, installer: ThemeInstaller, mode=None, is_filled=False):
        """
        :param preparation: Object responsible for theme extraction and preparation.
        :param installer: Object responsible for installing the theme.
        :param mode: Theme mode (e.g., 'light' or 'dark'). If not provided, both modes are used.
        :param is_filled: if True, theme will be filled
        """
        self.modes = [mode] if mode else ['light', 'dark']
        self.is_filled = is_filled

        self._preparation = preparation
        self._installer = installer

    @property
    def temp_folder(self):
        """The temporary folder path where the theme is prepared."""
        return self._preparation.temp_folder

    @property
    def destination_folder(self):
        """The destination folder path where the theme will be installed."""
        return self._installer.destination_folder

    @property
    def main_styles(self):
        """The path to the combined styles file generated during preparation."""
        return self._preparation.combined_styles_location

    @property
    def theme_name(self):
        return self._installer.theme_type

    def __add__(self, other: str) -> "Theme":
        """
        Appends additional styles to the main styles file.
        :param other: The additional styles to append.
        """
        self._preparation += other
        return self

    def __mul__(self, other: str) -> "Theme":
        """
        Adds a file to the theme, copying it to the temporary folder.
        :param other: The path of the file or folder to add.
        """
        self._preparation *= other
        return self

    def add_to_start(self, content) -> "Theme":
        """
        Inserts content at the beginning of the main styles file.
        :param content: The content to insert.
        """
        self._preparation.add_to_start(content)
        return self

    def add_from_file(self, content) -> "Theme":
        """
        Adds content from a file to the main styles file.
        :param content: The path of the file to add.
        """
        self._preparation.add_from_file(content)
        return self

    def prepare(self):
        """Extract theme from source folder and prepare it for installation."""
        self._preparation.prepare()
        if self.is_filled:
            self._preparation.replace_filled_keywords()

    def install(self, hue, name: str, sat: float | None = None, destination: str | None = None):
        """
        Installs the theme by applying the specified accent color and copying the finalized files
        to the designated destination.

        Args:
            hue: The hue value for the accent color (0-360 degrees).
            name: The name of the theme.
            sat: The saturation value for the accent color.
            destination: The custom folder where the theme will be installed.
        """
        theme_color = InstallationColor(
            hue=hue,
            saturation=sat,
            modes=self.modes
        )
        self._installer.install(theme_color, name, destination)