import os.path
import shutil
from unittest import TestCase
from unittest.mock import MagicMock

from scripts import config
from scripts.utils.global_theme.gdm_theme_prepare import GDMThemePrepare
from ..._helpers import create_dummy_file, try_remove_file


class GDMThemePrepareTestCase(TestCase):
    def setUp(self):
        self.temp_folder = os.path.join(config.temp_tests_folder, "gdm_theme_prepare")
        self.main_styles = os.path.join(self.temp_folder, "gnome-shell.css")
        self.theme = MagicMock()
        self.theme.add_to_start.return_value = None
        self.theme.temp_folder = self.temp_folder
        self.theme.main_styles = self.main_styles

        self.main_styles_destination = os.path.join(self.temp_folder, "gnome-shell-result.css")
        create_dummy_file(self.main_styles_destination, "body { background-color: #000; }")

        self.files_labeler = MagicMock()

        self.theme_prepare = GDMThemePrepare(
            theme=self.theme,
            theme_file=self.main_styles_destination,
            label=None,
            files_labeler=self.files_labeler,
        )

    def tearDown(self):
        shutil.rmtree(self.temp_folder, ignore_errors=True)

    def test_label_files_calls_labeler(self):
        self.theme_prepare.label = "dark"

        self.theme_prepare.label_theme()

        self.files_labeler.append_label.assert_called_once_with("dark")

    def test_label_files_raises_value_error_if_label_none(self):
        self.theme_prepare.label = None

        with self.assertRaises(ValueError):
            self.theme_prepare.label_theme()

    def test_remove_keywords_removes_destination_keywords(self):
        try_remove_file(self.main_styles_destination)
        expected_content = "body { background-color: #000; }"
        create_dummy_file(self.main_styles_destination, "body {keyword1 background-color: #000 !important; }")
        keywords = ["keyword1", " !important"]

        self.theme_prepare.remove_keywords(*keywords)

        with open(self.main_styles_destination, 'r') as file:
            content = file.read()
            self.assertEqual(content, expected_content)
        try_remove_file(self.main_styles_destination)

    def test_remove_properties_removes_destination_properties(self):
        try_remove_file(self.main_styles_destination)
        expected_content = "body {\n}\n"
        create_dummy_file(self.main_styles_destination, "body {\nbackground-color: #000;\n}")
        properties = ["background-color"]

        self.theme_prepare.remove_properties(*properties)

        with open(self.main_styles_destination, 'r') as file:
            actual_content = file.read()
            self.assertEqual(expected_content, actual_content)
        try_remove_file(self.main_styles_destination)

    def test_remove_properties_removes_one_line_properties(self):
        try_remove_file(self.main_styles_destination)
        expected_content = ""
        create_dummy_file(self.main_styles_destination, "body { background-color: #000; }")
        properties = ["background-color"]

        self.theme_prepare.remove_properties(*properties)

        with open(self.main_styles_destination, 'r') as file:
            actual_content = file.read()
            self.assertEqual(expected_content, actual_content)
        try_remove_file(self.main_styles_destination)

    def test_prepend_source_styles_prepends_destination_styles(self):
        try_remove_file(self.main_styles_destination)
        expected_content = "body { background-color: #000; }\n"
        create_dummy_file(self.main_styles_destination, "body { background-color: #000; }")

        self.theme_prepare.prepend_source_styles("")

        called_content: str = self.theme.add_to_start.call_args[0][0]
        self.assertTrue(called_content.startswith(expected_content))
        try_remove_file(self.main_styles_destination)

    def test_prepend_source_styles_adds_trigger(self):
        try_remove_file(self.main_styles_destination)
        expected_content = "\ntrigger\n"
        create_dummy_file(self.main_styles_destination)
        trigger = "trigger"

        self.theme_prepare.prepend_source_styles(trigger)

        called_content: str = self.theme.add_to_start.call_args[0][0]
        self.assertTrue(expected_content in called_content)
        try_remove_file(self.main_styles_destination)

    def test_install_passes_arguments_to_theme(self):
        hue = 0
        color = "#000000"
        sat = 100
        destination = os.path.join(self.temp_folder, "destination")

        self.theme_prepare.install(hue, color, sat, destination)

        self.theme.install.assert_called_once_with(hue, color, sat, destination=destination)