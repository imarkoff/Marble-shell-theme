# TODO: Add more tests

import unittest
import os
import json
import shutil
from unittest.mock import patch

from . import config
from .theme import Theme

# folders
tests_folder = '.tests'
project_folder = '.'


class TestInstall(unittest.TestCase):
    def setUp(self):
        # Create necessary directories
        os.makedirs(f"{project_folder}/{config.raw_theme_folder}/{config.gnome_folder}", exist_ok=True)
        os.makedirs(f"{tests_folder}/.themes", exist_ok=True)
        os.makedirs(f"{tests_folder}/.temp", exist_ok=True)

    def tearDown(self):
        # Clean up after tests
        shutil.rmtree(tests_folder, ignore_errors=True)

    @patch('scripts.utils.gnome.subprocess.check_output')
    def test_install_theme(self, mock_check_output):
        """
        Test if theme is installed correctly (colors are replaced)
        """
        mock_check_output.return_value = 'GNOME Shell 47.0\n'

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
