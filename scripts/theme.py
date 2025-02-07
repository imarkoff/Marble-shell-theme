import os
import shutil
import colorsys  # colorsys.hls_to_rgb(h, l, s)

from .utils import (
    replace_keywords,    # replace keywords in file
    copy_files,          # copy files from source to destination
    destination_return,  # copied/modified theme location
    generate_file)       # combine files from folder to one file


class Theme:
    def __init__(self, theme_type, colors_json, theme_folder, destination_folder, temp_folder,
                 mode=None, is_filled=False):
        """
        Initialize Theme class
        :param colors_json: location of a json file with colors
        :param theme_type: theme type (gnome-shell, gtk, etc.)
        :param theme_folder: raw theme location
        :param destination_folder: folder where themes will be installed
        :param temp_folder: folder where files will be collected
        :param mode: theme mode (light or dark)
        :param is_filled: if True, theme will be filled
        """

        self.colors = colors_json
        self.temp_folder = f"{temp_folder}/{theme_type}"
        self.theme_folder = theme_folder
        self.theme_type = theme_type
        self.mode = [mode] if mode else ['light', 'dark']
        self.destination_folder = destination_folder
        self.main_styles = f"{self.temp_folder}/{theme_type}.css"

        # move files to temp folder
        copy_files(self.theme_folder, self.temp_folder)
        generate_file(f"{self.theme_folder}", self.main_styles)
        # after generating main styles, remove .css and .versions folders
        shutil.rmtree(f"{self.temp_folder}/.css/", ignore_errors=True)
        shutil.rmtree(f"{self.temp_folder}/.versions/", ignore_errors=True)

        # if theme is filled
        if is_filled:
            for apply_file in os.listdir(f"{self.temp_folder}/"):
                replace_keywords(f"{self.temp_folder}/{apply_file}",
                                 ("BUTTON-COLOR", "ACCENT-FILLED-COLOR"),
                                 ("BUTTON_HOVER", "ACCENT-FILLED_HOVER"),
                                 ("BUTTON_ACTIVE", "ACCENT-FILLED_ACTIVE"),
                                 ("BUTTON_INSENSITIVE", "ACCENT-FILLED_INSENSITIVE"),
                                 ("BUTTON-TEXT-COLOR", "TEXT-BLACK-COLOR"),
                                 ("BUTTON-TEXT_SECONDARY", "TEXT-BLACK_SECONDARY"))

    def __add__(self, other):
        """
        Add to main styles another styles
        :param other: styles to add
        :return: new Theme object
        """

        with open(self.main_styles, 'a') as main_styles:
            main_styles.write('\n' + other)
        return self

    def __mul__(self, other):
        """
        Copy files to temp folder
        :param other: file or folder
        :return: new Theme object
        """

        if os.path.isfile(other):
            shutil.copy(other, self.temp_folder)
        else:
            shutil.copytree(other, self.temp_folder)

        return self

    def __del__(self):
        # delete temp folder
        os.system(f"rm -r {self.temp_folder}")

    def __apply_colors(self, hue, destination, theme_mode, apply_file, sat=None):
        """
        Install accent colors from colors.json to different file
        :param hue
        :param destination: file directory
        :param theme_mode: theme name (light or dark)
        :param apply_file: file name
        :param sat: color saturation (optional)
        """

        # list of (keyword, replaced value)
        replaced_colors = list()

        # colorsys works in range(0, 1)
        h = hue / 360
        for element in self.colors["elements"]:
            # if color has default color and hasn't been replaced
            if theme_mode not in self.colors["elements"][element] and self.colors["elements"][element]["default"]:
                default_element = self.colors["elements"][element]["default"]
                default_color = self.colors["elements"][default_element][theme_mode]
                self.colors["elements"][element][theme_mode] = default_color

            # convert sla to range(0, 1)
            lightness = int(self.colors["elements"][element][theme_mode]["l"]) / 100
            saturation = int(self.colors["elements"][element][theme_mode]["s"]) / 100 if sat is None else \
                int(self.colors["elements"][element][theme_mode]["s"]) * (sat / 100) / 100
            alpha = self.colors["elements"][element][theme_mode]["a"]

            # convert hsl to rgb and multiply every item
            red, green, blue = [int(item * 255) for item in colorsys.hls_to_rgb(h, lightness, saturation)]

            replaced_colors.append((element, f"rgba({red}, {green}, {blue}, {alpha})"))

        # replace colors
        replace_keywords(os.path.expanduser(f"{destination}/{apply_file}"), *replaced_colors)

    def __apply_theme(self, hue, source, destination, theme_mode, sat=None):
        """
        Apply theme to all files in directory
        :param hue
        :param source
        :param destination: file directory
        :param theme_mode: theme name (light or dark)
        :param sat: color saturation (optional)
        """

        for apply_file in os.listdir(f"{source}/"):
            self.__apply_colors(hue, destination, theme_mode, apply_file, sat=sat)

    def install(self, hue, name, sat=None, destination=None):
        """
        Copy files and generate theme with different accent color
        :param hue
        :param name: theme name
        :param sat: color saturation (optional)
        :param destination: folder where theme will be installed
        """

        is_dest = bool(destination)

        print(f"Creating {name} {', '.join(self.mode)} theme...", end=" ")

        try:
            for mode in self.mode:
                if not is_dest:
                    destination = destination_return(self.destination_folder, name, mode, self.theme_type)

                copy_files(self.temp_folder + '/', destination)
                self.__apply_theme(hue, self.temp_folder, destination, mode, sat=sat)

        except Exception as err:
            print("\nError: " + str(err))

        else:
            print("Done.")

    def add_to_start(self, content):
        """
        Add content to the start of main styles
        :param content: content to add
        """

        with open(self.main_styles, 'r') as main_styles:
            main_content = main_styles.read()

        with open(self.main_styles, 'w') as main_styles:
            main_styles.write(content + '\n' + main_content)
