# TODO: Add more tests

import unittest
import os
import json
import shutil

from . import config
from .theme import Theme

# folders
tests_folder = '.tests'
project_folder = '.'


class TestInstall(unittest.TestCase):

    def test_install_theme(self):
        """
        Test if theme is installed correctly (colors are replaced)
        """

        # folders
        themes_folder = f"{tests_folder}/.themes"
        temp_folder = f"{tests_folder}/.temp"

        # colors from colors.json
        colors_json = open(f"{project_folder}/{config.colors_json}")
        colors = json.load(colors_json)
        colors_json.close()

        # create test theme
        test_theme = Theme("gnome-shell", colors,
                           f"{project_folder}/{config.raw_theme_folder}/{config.gnome_folder}",
                           themes_folder, temp_folder,
                           mode='light', is_filled=True)

        # install test theme
        test_theme.install(120, 'test', 70)

        # folder with installed theme (.tests/.themes/Marble-test-light/gnome-shell)
        installed_theme = f"{themes_folder}/{os.listdir(themes_folder)[0]}/{config.gnome_folder}"

        # check if files are installed
        for file in os.listdir(installed_theme):
            with open(f"{installed_theme}/{file}") as f:
                read_file = f.read()

                for color in colors["elements"]:
                    self.assertNotIn(color, read_file, msg=f"Color {color} is not replaced in {file}")

        # delete test theme
        del test_theme
        shutil.rmtree(tests_folder)


if __name__ == '__main__':
    unittest.main()
