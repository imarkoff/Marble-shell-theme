import functools
import os
import subprocess
from typing import Optional, TypeAlias

from .theme import Theme
from .utils import remove_properties, remove_keywords
from . import config
from .utils.console import Console, Color, Format
from .utils.files_labeler import FilesLabeler

Path: TypeAlias = str | bytes


class ThemePrepare:
    """
    Theme object prepared for installation
    """

    def __init__(self, theme: Theme, theme_file, label: Optional[str] = None):
        self.theme = theme
        self.theme_file = theme_file
        self.label = label


class GlobalTheme:
    def __init__(self, colors_json, theme_folder, destination_folder, destination_file, temp_folder: str,
                 mode=None, is_filled=False):
        """
        Initialize GlobalTheme class
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

        self.backup_file = f"{self.destination_file}.backup"
        self.backup_trigger = "\n/* Marble theme */\n"
        self.extracted_theme: str = os.path.join(self.temp_folder, config.extracted_gdm_folder)
        self.gresource_file = os.path.join(self.destination_folder, self.destination_file)

        self.themes: list[ThemePrepare] = []
        self.is_filled = is_filled
        self.mode = mode

    def prepare(self):
        self.__extract()
        self.__find_themes()

    def __extract(self):
        """Extract gresource files to temp folder"""
        extract_line = Console.Line()
        extract_line.update("Extracting gresource files...")

        resources_list_response = subprocess.run(
            ["gresource", "list", self.gresource_file],
            capture_output=True, text=True, check=False
        )

        if resources_list_response.stderr:
            extract_line.error(f"Failed to extract resources: {resources_list_response.stderr.strip()}")
            raise Exception(f"gresource could not process the theme file: {self.gresource_file}")

        resources = resources_list_response.stdout.strip().split("\n")
        prefix = "/org/gnome/shell/theme/"

        try:
            for resource in resources:
                resource_path = resource.replace(prefix, "")
                output_path = os.path.join(self.extracted_theme, resource_path)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                with open(output_path, 'wb') as f:
                    subprocess.run(["gresource", "extract", self.gresource_file, resource], stdout=f, check=True)

            extract_line.success("Extracted gresource files.")

        except FileNotFoundError as e:
            if "gresource" in str(e):
                self.__raise_gresource_error(e)
            raise

    @staticmethod
    def __raise_gresource_error(e: Exception):
        print("Error: 'gresource' command not found.")
        print("Please install the glib2-devel package:")
        print(" - For Fedora/RHEL: sudo dnf install glib2-devel")
        print(" - For Ubuntu/Debian: sudo apt install libglib2.0-dev")
        print(" - For Arch: sudo pacman -S glib2-devel")
        raise Exception("Missing required dependency: glib2-devel") from e

    def __find_themes(self):
        extracted_theme_files = os.listdir(self.extracted_theme)

        allowed_modes = ("dark", "light")
        allowed_css = ("gnome-shell-dark", "gnome-shell-light", "gnome-shell")

        for style_name in allowed_css:
            style_file = style_name + ".css"
            if style_file in extracted_theme_files:
                last_mode = style_name.split("-")[-1]
                mode = last_mode if last_mode in allowed_modes else None
                self.__append_theme(style_name, mode=mode or self.mode, label=mode)

    def __append_theme(self, theme_type: str, mode=None, label: Optional[str] = None):
        """Helper to create theme objects"""
        theme = Theme(theme_type, self.colors_json, self.theme_folder,
                      self.extracted_theme, self.temp_folder,
                      mode=mode, is_filled=self.is_filled)
        theme.prepare()
        theme_file = os.path.join(self.extracted_theme, f"{theme_type}.css")
        self.themes.append(ThemePrepare(theme=theme, theme_file=theme_file, label=label))

    def install(self, hue, sat=None):
        """Install theme globally"""
        if os.geteuid() != 0:
            raise Exception("Root privileges required to install GDM theme")

        if self.__is_installed():
            Console.Line().info("Theme is installed. Reinstalling...")
            self.gresource_file += ".backup"

        self.__generate_themes(hue, 'Marble', sat)
        self.__backup()

        # generate gnome-shell-theme.gresource.xml
        with open(f"{self.extracted_theme}/{self.destination_file}.xml", 'w') as gresource_xml:
            generated_xml = self.__generate_gresource_xml()
            gresource_xml.write(generated_xml)
        self.__compile_resources()

        install_line = Console.Line()
        install_line.update("Moving compiled theme to system folder...")
        subprocess.run(["sudo", "cp", "-f",
                        f"{self.extracted_theme}/{self.destination_file}",
                        f"{self.destination_folder}/{self.destination_file}"],
                       check=True)
        install_line.success("Theme moved to system folder.")

        self.__update_alternatives()

    def __is_installed(self) -> bool:
        with open(self.gresource_file, "rb") as f:
            return self.backup_trigger.encode() in f.read()

    def __generate_themes(self, hue: int, color: str, sat: Optional[int]=None):
        """Generate theme files for gnome-shell-theme.gresource.xml"""
        for theme_prepare in self.themes:
            if theme_prepare.label is not None:
                temp_folder = theme_prepare.theme.temp_folder
                main_styles = theme_prepare.theme.main_styles
                FilesLabeler(temp_folder, main_styles).append_label(theme_prepare.label)

            remove_keywords(theme_prepare.theme_file, "!important")
            remove_properties(theme_prepare.theme_file, "background-color", "color", "box-shadow", "border-radius")

            self.__add_gnome_styles(theme_prepare.theme)

            theme_prepare.theme.install(hue, color, sat, destination=self.extracted_theme)

    def __add_gnome_styles(self, theme: Theme):
        """Add gnome styles to the start of the file"""
        with open(f"{theme.destination_folder}/{theme.theme_type}.css", 'r') as gnome_theme:
            gnome_styles = gnome_theme.read() + self.backup_trigger
            theme.add_to_start(gnome_styles)

    def __backup(self):
        if self.__is_installed():
            return

        backup_line = Console.Line()

        backup_line.update("Backing up default theme...")
        subprocess.run(["cp", "-aT", self.gresource_file, f"{self.gresource_file}.backup"],
                       cwd=self.destination_folder, check=True)
        backup_line.success("Backed up default theme.")

    def __generate_gresource_xml(self):
        files_to_include = []
        for root, dirs, filenames in os.walk(self.extracted_theme):
            for filename in filenames:
                # Get a path relative to extracted_theme directory
                full_path = os.path.join(root, filename)
                rel_path = os.path.relpath(full_path, self.extracted_theme)
                files_to_include.append(f"<file>{rel_path}</file>")
        nl = "\n"  # fstring doesn't support newline character

        return f"""<?xml version="1.0" encoding="UTF-8"?>
<gresources>
    <gresource prefix="/org/gnome/shell/theme">
        {nl.join(files_to_include)}
    </gresource>
</gresources>"""

    def __compile_resources(self):
        compile_line = Console.Line()
        compile_line.update("Compiling gnome-shell theme...")

        try:
            subprocess.run(["glib-compile-resources",
                            "--sourcedir", self.extracted_theme,
                            "--target", f"{self.extracted_theme}/{self.destination_file}",
                            f"{self.destination_file}.xml"
                            ],
                           cwd=self.extracted_theme, check=True)
        except FileNotFoundError as e:
            if "glib-compile-resources" in str(e):
                self.__raise_gresource_error(e)
            raise

        compile_line.success("Theme compiled.")

    def __update_alternatives(self):
        link = os.path.join(self.destination_folder, config.ubuntu_gresource_link)
        name = config.ubuntu_gresource_link
        path = os.path.join(self.destination_folder, self.destination_file)
        AlternativesUpdater.install_and_set(link, name, path)

    def remove(self):
        if self.__is_installed():
            removing_line = Console.Line()
            removing_line.update("Theme is installed. Removing...")
            backup_path = os.path.join(self.destination_folder, self.backup_file)
            dest_path = os.path.join(self.destination_folder, self.destination_file)

            if os.path.isfile(backup_path):
                subprocess.run(["sudo", "mv", backup_path, dest_path], check=True)
                removing_line.success("Global theme removed successfully. Restart GDM to apply changes.")

            else:
                formatted_shell = Console.format("gnome-shell", color=Color.BLUE, format_type=Format.BOLD)
                removing_line.error(f"Backup file not found. Try reinstalling {formatted_shell} package.")

        else:
            Console.Line().error("Theme is not installed. Nothing to remove.")
            Console.Line().warn("If theme is still installed globally, try reinstalling gnome-shell package.")

    def __remove_alternatives(self):
        name = config.ubuntu_gresource_link
        path = os.path.join(self.destination_folder, self.destination_file)
        AlternativesUpdater.remove(name, path)


class AlternativesUpdater:
    @staticmethod
    def ubuntu_specific(func):
        """
        Decorator for Ubuntu-specific functionality.
        Silently ignores errors when not running on Ubuntu systems.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except FileNotFoundError as e:
                if not "update-alternatives" in str(e):
                    raise
                return None

        return wrapper

    @staticmethod
    @ubuntu_specific
    def install_and_set(link: str, name: str, path: Path, priority: int = 0):
        AlternativesUpdater.install(link, name, path, priority)
        AlternativesUpdater.set(name, path)

    @staticmethod
    @ubuntu_specific
    def install(link: str, name: str, path: Path, priority: int = 0):
        """
        Add an alternative to the system
        :param link: Absolute path with file name where the link will be created
        :param name: Name of the alternative
        :param path: An absolute path to the file that will be linked
        :param priority: Priority of the alternative; Higher number means higher priority

        Example:
            install(/usr/share/gnome-shell/gdm-theme.gresource,
            gdm-theme.gresource, /usr/share/gnome-shell/gnome-shell-theme.gresource)
        """
        subprocess.run([
            "update-alternatives", "--quiet", "--install",
            link, name, str(path), str(priority)
        ], check=True)
        Console.Line().success(f"Installed {name} alternative.")

    @staticmethod
    @ubuntu_specific
    def set(name: str, path: Path):
        """
        Set path as alternative to name in system
        :param name: Name of the alternative
        :param path: An absolute path to the file that will be linked

        Example:
            set(gdm-theme.gresource, /usr/share/gnome-shell/gnome-shell-theme.gresource)
        """
        subprocess.run([
            "update-alternatives", "--quiet", "--set",
            name, str(path)
        ], check=True)

    @staticmethod
    @ubuntu_specific
    def remove(name: str, path: Path):
        """
        Remove alternative from system
        :param name: Name of the alternative
        :param path: An absolute path to the file that will be linked

        Example:
            remove(gdm-theme.gresource, /usr/share/gnome-shell/gnome-shell-theme.gresource)
        """
        subprocess.run([
            "update-alternatives", "--quiet", "--remove",
            name, str(path)
        ], check=True)
        Console.Line().success(f"Removed {name} alternative.")