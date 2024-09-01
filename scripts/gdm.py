import os
import subprocess
import shutil

from .theme import Theme
from .utils import label_files, remove_properties, remove_keywords
from . import config


class GlobalTheme:
    def __init__(self, colors_json, theme_folder, destination_folder, destination_file, temp_folder,
                 is_filled=False):
        """
        Initialize GlobalTheme class
        :param colors_json: location of a json file with colors
        :param theme_folder: raw theme location
        :param destination_folder: folder where themes will be installed
        :param temp_folder: folder where files will be collected
        :param is_filled: if True, theme will be filled
        """

        self.colors_json = colors_json
        self.theme_folder = theme_folder
        self.destination_folder = destination_folder
        self.destination_file = destination_file
        self.temp_folder = f"{temp_folder}/gdm"

        self.backup_file = f"{self.destination_file}.backup"
        self.backup_trigger = "\n/* Marble theme */\n"  # trigger to check if theme is installed
        self.extracted_theme = f"{self.temp_folder}/{config.extracted_gdm_folder}"
        self.gst = f"{self.destination_folder}/{self.destination_file}"  # use backup file if theme is installed
        self.extracted_light_theme = f"{self.extracted_theme}/gnome-shell-light.css"
        self.extracted_dark_theme = f"{self.extracted_theme}/gnome-shell-dark.css"

        os.makedirs(self.temp_folder, exist_ok=True)  # create temp folder

        # create light and dark themes
        self.light_theme = Theme("gnome-shell-light", self.colors_json, self.theme_folder,
                                 self.extracted_theme, self.temp_folder, mode='light', is_filled=is_filled)
        self.dark_theme = Theme("gnome-shell-dark", self.colors_json, self.theme_folder,
                                self.extracted_theme, self.temp_folder, mode='dark', is_filled=is_filled)

    def __del__(self):
        """
        Delete temp folder
        """

        del self.light_theme
        del self.dark_theme

        shutil.rmtree(self.temp_folder)

    def __is_installed(self):
        """
        Check if theme is installed
        :return: True if theme is installed, False otherwise
        """

        with open(f"{self.destination_folder}/{self.destination_file}", "rb") as f:
            content = f.read()
            return self.backup_trigger.encode() in content

    def __extract(self):
        """
        Extract gresource files to temp folder
        """

        print("Extracting gresource files...")

        gst = self.gst
        workdir = self.temp_folder

        # Get the list of resources
        resources = subprocess.getoutput(f"gresource list {gst}").split("\n")

        # Create directories
        for r in resources:
            r = r.replace("/org/gnome/shell/", "")
            directory = os.path.join(workdir, os.path.dirname(r))
            os.makedirs(directory, exist_ok=True)

        # Extract resources
        for r in resources:
            output_path = os.path.join(workdir, r.replace("/org/gnome/shell/", ""))
            subprocess.run(f"gresource extract {gst} {r} > {output_path}", shell=True)

    def __add_gnome_styles(self, theme):
        """
        Add gnome styles to the start of the file
        :param theme: Theme object
        """

        with open(f"{self.extracted_theme}/{theme.theme_type}.css", 'r') as gnome_theme:
            gnome_styles = gnome_theme.read() + self.backup_trigger
            theme.add_to_start(gnome_styles)

    def __prepare(self, hue, color, sat=None):
        """
        Generate theme files for gnome-shell-theme.gresource.xml
        :param hue: color hue
        :param color: color name
        :param sat: color saturation
        """

        # add -light label to light theme files because they are installed to the same folder
        label_files(self.light_theme.temp_folder, "light", self.light_theme.main_styles)

        # remove !important from the gnome file
        remove_keywords(self.extracted_light_theme, "!important")
        remove_keywords(self.extracted_dark_theme, "!important")

        # remove properties from the gnome file
        props_to_remove = ("background-color", "color", "box-shadow", "border-radius")
        remove_properties(self.extracted_light_theme, *props_to_remove)
        remove_properties(self.extracted_dark_theme, *props_to_remove)

        # add gnome styles to the start of the file
        self.__add_gnome_styles(self.light_theme)
        self.__add_gnome_styles(self.dark_theme)

        # build code for gnome-shell-theme.gresource.xml
        self.light_theme.install(hue, color, sat, destination=self.extracted_theme)
        self.dark_theme.install(hue, color, sat, destination=self.extracted_theme)

    def __backup(self):
        """
        Backup installed theme
        """

        if self.__is_installed():
            return

        # backup installed theme
        print("Backing up default theme...")
        os.system(f"cp -aT {self.gst} {self.gst}.backup")

    def __generte_gresource_xml(self):
        """
        Generates.gresource.xml
        """

        # list of files to add to gnome-shell-theme.gresource.xml
        files = list(f"<file>{file}</file>" for file in os.listdir(self.extracted_theme))
        nl = "\n"  # fstring doesn't support newline character

        ready_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<gresources>
    <gresource prefix="/org/gnome/shell/theme">
        {nl.join(files)}
    </gresource>
</gresources>"""

        return ready_xml

    def install(self, hue, sat=None):
        """
        Install theme globally
        :param hue: color hue
        :param sat: color saturation
        """

        if os.geteuid() != 0:
            raise Exception("Root privileges required to install GDM theme")

        if self.__is_installed():
            print("Theme is installed. Reinstalling...")
            self.gst += ".backup"

        self.__extract()

        # generate theme files for global theme
        self.__prepare(hue, 'Marble', sat)

        # generate gnome-shell-theme.gresource.xml
        with open(f"{self.extracted_theme}/{self.destination_file}.xml", 'w') as gresource_xml:
            generated_xml = self.__generte_gresource_xml()
            gresource_xml.write(generated_xml)

        # compile gnome-shell-theme.gresource.xml
        print("Compiling theme...")
        subprocess.run(f"glib-compile-resources {self.destination_file}.xml",
                       shell=True, cwd=self.extracted_theme)

        # backup installed theme
        self.__backup()

        # install theme
        print("Installing theme...")
        subprocess.run(["sudo", "cp", "-f", 
                        f"{self.extracted_theme}/{self.destination_file}", 
                        f"{self.destination_folder}/{self.destination_file}"], 
                       check=True)

        return 0

    def remove(self):
        """
        Remove installed theme
        """

        # use backup file if theme is installed
        if self.__is_installed():
            print("Theme is installed. Removing...")

            if os.path.isfile(f"{self.destination_folder}/{self.backup_file}"):
                subprocess.run(f"sudo mv {self.backup_file} {self.destination_file}",
                               shell=True, cwd=self.destination_folder)

            else:
                print("Backup file not found. Try reinstalling gnome-shell package.")
                return 1

        else:
            print("Theme is not installed. Nothing to remove.")
            print("If theme is still installed globally, try reinstalling gnome-shell package.")
            return 1

        return 0
