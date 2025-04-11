import os.path
import shutil
import unittest
from unittest.mock import Mock

from scripts import config
from scripts.utils.theme.theme_color_applier import ThemeColorApplier
from ..._helpers import create_dummy_file


class ThemeColorApplierTestCase(unittest.TestCase):
    def setUp(self):
        color_replacement_generator = Mock()
        color_replacement_generator.convert.return_value = [
            ("ACCENT-COLOR", "rgba(255, 0, 0, 1)"),
            ("ACCENT_HOVER", "rgba(255, 0, 0, 0.8)"),
            ("BACKGROUND-COLOR", "rgba(0, 0, 0, 1)")
        ]

        self.temp_folder = os.path.join(config.temp_tests_folder, "color_applier")
        self._setup_temp_folder()

        self.color_applier = ThemeColorApplier(color_replacement_generator)

    def tearDown(self):
        shutil.rmtree(self.temp_folder, ignore_errors=True)

    def _setup_temp_folder(self):
        self.first_file = os.path.join(self.temp_folder, "file1.css")
        self.second_file = os.path.join(self.temp_folder, "file2.css")
        self.first_css = "body { background-color: ACCENT-COLOR; color: ACCENT_HOVER; }"
        self.second_css = "body { background-color: BACKGROUND-COLOR; }"
        create_dummy_file(self.first_file, self.first_css)
        create_dummy_file(self.second_file, self.second_css)

    def test_colors_in_files_are_replaced_correctly(self):
        theme_color = Mock()

        self.color_applier.apply(theme_color, self.temp_folder, "dark")

        with open(self.first_file, "r") as file:
            content = file.read()
            replaced = self.first_css
            replaced = replaced.replace("ACCENT-COLOR", "rgba(255, 0, 0, 1)")
            replaced = replaced.replace("ACCENT_HOVER", "rgba(255, 0, 0, 0.8)")
            assert content == replaced

        with open(self.second_file, "r") as file:
            content = file.read()
            replaced = self.second_css
            replaced = replaced.replace("BACKGROUND-COLOR", "rgba(0, 0, 0, 1)")
            assert content == replaced