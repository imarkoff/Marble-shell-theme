import os
from typing import Optional

from .install.colors_definer import ColorsDefiner
from .theme import Theme
from .utils import remove_properties, remove_keywords
from . import config
from .utils.alternatives_updater import AlternativesUpdater
from .utils.console import Console, Color, Format
from .utils.files_labeler import FilesLabeler
from .utils.gresource import Gresource, GresourceBackupNotFoundError


class GlobalTheme:
    """Class to install global theme for GDM"""
    def __init__(self,
                 colors_json: ColorsDefiner, theme_folder: str,
                 destination_folder: str, destination_file: str, temp_folder: str,
                 mode: Optional[str] = None, is_filled = False
                 ):
        """
        :param colors_json: location of a JSON file with color values
        :param theme_folder: raw theme location
        :param destination_folder: folder where themes will be installed
        :param temp_folder: folder where files will be collected
        :param mode: theme mode (light or dark)
        :param is_filled: if True, the theme will be filled
        """
        self.colors_json = colors_json
        self.theme_folder = theme_folder
        self.destination_folder = destination_folder
        self.destination_file = destination_file
        self.temp_folder = temp_folder
        self.is_filled = is_filled
        self.mode = mode

        self.themes: list[ThemePrepare] = []

        self.__is_installed_trigger = "\n/* Marble theme */\n"
        self.__gresource_file = os.path.join(self.destination_folder, self.destination_file)

        self.__gresource_temp_folder = os.path.join(self.temp_folder, config.extracted_gdm_folder)
        self.__gresource = Gresource(self.destination_file, self.__gresource_temp_folder, self.destination_folder)

    def prepare(self):
        if self.__is_installed():
            Console.Line().info("Theme is installed. Reinstalling...")
            self.__gresource.use_backup_gresource()

        self.__gresource.extract()
        self.__find_themes()

    def __is_installed(self) -> bool:
        if not hasattr(self, '__is_installed_cached'):
            with open(self.__gresource_file, "rb") as f:
                self.__is_installed_cached = self.__is_installed_trigger.encode() in f.read()

        return self.__is_installed_cached

    def __find_themes(self):
        extracted_theme_files = os.listdir(self.__gresource_temp_folder)

        allowed_modes = ("dark", "light")
        allowed_css = ("gnome-shell-dark", "gnome-shell-light", "gnome-shell")

        for style_name in allowed_css:
            style_file = style_name + ".css"
            if style_file in extracted_theme_files:
                last_mode = style_name.split("-")[-1]
                mode = last_mode if last_mode in allowed_modes else None
                self.__append_theme(style_name, mode=mode or self.mode, label=mode)

    def __append_theme(self, theme_type: str, mode = None, label: Optional[str] = None):
        """Helper to create theme objects"""
        theme = Theme(theme_type, self.colors_json, self.theme_folder,
                      self.__gresource_temp_folder, self.temp_folder,
                      mode=mode, is_filled=self.is_filled)
        theme.prepare()
        theme_file = os.path.join(self.__gresource_temp_folder, f"{theme_type}.css")
        self.themes.append(ThemePrepare(theme=theme, theme_file=theme_file, label=label))

    def install(self, hue, sat=None):
        """Install theme globally"""
        if os.geteuid() != 0:
            raise Exception("Root privileges required to install GDM theme")

        self.__generate_themes(hue, 'Marble', sat)

        self.__gresource.compile()
        if not self.__is_installed():
            self.__gresource.backup()
        self.__gresource.move()

        self.__update_alternatives()

    def __generate_themes(self, hue: int, color: str, sat: Optional[int] = None):
        """Generate theme files for gnome-shell-theme.gresource.xml"""
        for theme_prepare in self.themes:
            if theme_prepare.label is not None:
                temp_folder = theme_prepare.theme.temp_folder
                main_styles = theme_prepare.theme.main_styles
                FilesLabeler(temp_folder, main_styles).append_label(theme_prepare.label)

            remove_keywords(theme_prepare.theme_file, "!important")
            remove_properties(theme_prepare.theme_file, "background-color", "color", "box-shadow", "border-radius")

            self.__add_gnome_styles(theme_prepare.theme)

            theme_prepare.theme.install(hue, color, sat, destination=self.__gresource_temp_folder)

    def __add_gnome_styles(self, theme: Theme):
        """Add gnome styles to the start of the file"""
        with open(f"{theme.destination_folder}/{theme.theme_type}.css", 'r') as gnome_theme:
            gnome_styles = gnome_theme.read() + self.__is_installed_trigger
            theme.add_to_start(gnome_styles)

    def __update_alternatives(self):
        link = os.path.join(self.destination_folder, config.ubuntu_gresource_link)
        name = config.ubuntu_gresource_link
        path = os.path.join(self.destination_folder, self.destination_file)
        AlternativesUpdater.install_and_set(link, name, path)

    def remove(self):
        if self.__is_installed():
            removing_line = Console.Line()
            removing_line.update("Theme is installed. Removing...")

            try:
                self.__gresource.restore()
                removing_line.success("Global theme removed successfully. Restart GDM to apply changes.")
            except GresourceBackupNotFoundError:
                formatted_shell = Console.format("gnome-shell", color=Color.BLUE, format_type=Format.BOLD)
                removing_line.error(f"Backup file not found. Try reinstalling {formatted_shell} package.")
        else:
            Console.Line().error("Theme is not installed. Nothing to remove.")
            Console.Line().warn("If theme is still installed globally, try reinstalling gnome-shell package.")

    def __remove_alternatives(self):
        name = config.ubuntu_gresource_link
        path = os.path.join(self.destination_folder, self.destination_file)
        AlternativesUpdater.remove(name, path)


class ThemePrepare:
    """Theme data class prepared for installation"""
    def __init__(self, theme: Theme, theme_file, label: Optional[str] = None):
        self.theme = theme
        self.theme_file = theme_file
        self.label = label