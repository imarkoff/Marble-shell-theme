import os
import shutil
import unittest
from unittest.mock import patch

from scripts import config
from scripts.utils.style_manager import StyleManager
from .._helpers import create_dummy_file


class StyleManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_folder = os.path.join(config.temp_tests_folder, "style_manager")
        os.makedirs(self.temp_folder, exist_ok=True)
        self.output_file = os.path.join(self.temp_folder, "output.css")
        self.manager = StyleManager(output_file=self.output_file)

    def tearDown(self):
        shutil.rmtree(self.temp_folder, ignore_errors=True)

    def test_append_content(self):
        start_css = "body { background-color: blue; }"
        create_dummy_file(self.output_file, start_css)
        end_css = "h1 { color: red; }"

        self.manager.append_content(end_css)

        with open(self.output_file, 'r') as f:
            content = f.read()
            split_content = content.splitlines()
            assert split_content[0] == start_css
            assert split_content[1] == end_css
        os.remove(self.output_file)

    def test_append_does_not_create_file(self):
        end_css = "h1 { color: red; }"

        with self.assertRaises(FileNotFoundError):
            self.manager.append_content(end_css)

    def test_prepend_content(self):
        start_css = "body { background-color: blue; }"
        create_dummy_file(self.output_file, start_css)
        prepend_css = "h1 { color: red; }"

        self.manager.prepend_content(prepend_css)

        with open(self.output_file, 'r') as f:
            content = f.read()
            split_content = content.splitlines()
            assert split_content[0] == prepend_css
            assert split_content[1] == start_css
        os.remove(self.output_file)

    def test_prepend_does_not_create_file(self):
        prepend_css = "h1 { color: red; }"

        with self.assertRaises(FileNotFoundError):
            self.manager.prepend_content(prepend_css)

    def test_generate_combined_styles(self):
        source_folder = os.path.join(config.temp_tests_folder, "style_manager_source")
        source_css_folder = os.path.join(source_folder, ".css")
        first_file = os.path.join(source_css_folder, "file1.css")
        second_file = os.path.join(source_css_folder, "file2.css")
        first_css = "body { background-color: blue; }"
        second_css = "h1 { color: red; }"
        create_dummy_file(first_file, first_css)
        create_dummy_file(second_file, second_css)

        with patch("subprocess.check_output", return_value="GNOME Shell 47.0"):
            self.manager.generate_combined_styles(source_folder, self.temp_folder)

        with open(self.output_file, 'r') as f:
            content = f.read()
            split_content = content.splitlines()
            assert first_css in split_content
            assert second_css in split_content
        os.remove(self.output_file)
        shutil.rmtree(source_folder, ignore_errors=True)