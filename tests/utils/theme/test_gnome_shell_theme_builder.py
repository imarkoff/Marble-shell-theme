import unittest
from unittest.mock import Mock
import os

from scripts.utils.theme.gnome_shell_theme_builder import GnomeShellThemeBuilder


class GnomeShellThemeBuilderTestCase(unittest.TestCase):
    def setUp(self):
        self.colors_provider = Mock()
        self.builder = GnomeShellThemeBuilder(self.colors_provider)

    def test_builder_method_chaining_works_correctly(self):
        result = (self.builder.with_theme_name("test-theme")
                  .with_mode("dark")
                  .filled()
                  .with_temp_folder("/tmp/test"))

        self.assertIs(result, self.builder)
        self.assertEqual("test-theme", self.builder.theme_name)
        self.assertEqual("dark", self.builder.mode)
        self.assertTrue(self.builder.is_filled)
        self.assertEqual("/tmp/test", self.builder._base_temp_folder)

    def test_paths_update_when_base_folder_changes(self):
        self.builder.with_temp_folder("/custom/temp")

        expected_temp_folder = os.path.join("/custom/temp", self.builder.theme_name)
        expected_main_styles = os.path.join(expected_temp_folder, f"{self.builder.theme_name}.css")

        self.assertEqual(expected_temp_folder, self.builder.temp_folder)
        self.assertEqual(expected_main_styles, self.builder.main_styles)

    def test_paths_update_when_theme_name_changes(self):
        original_temp_folder = self.builder.temp_folder
        original_main_styles = self.builder.main_styles

        self.builder.with_theme_name("custom-theme")

        self.assertNotEqual(original_temp_folder, self.builder.temp_folder)
        self.assertNotEqual(original_main_styles, self.builder.main_styles)
        self.assertEqual(os.path.join(self.builder._base_temp_folder, "custom-theme"), self.builder.temp_folder)
        self.assertEqual(os.path.join(self.builder.temp_folder, "custom-theme.css"), self.builder.main_styles)

    def test_default_values_are_set_properly(self):
        builder = GnomeShellThemeBuilder(self.colors_provider)

        self.assertEqual("gnome-shell", builder.theme_name)
        self.assertIsNone(builder.mode)
        self.assertFalse(builder.is_filled)
        self.assertIsNone(builder.preparation)
        self.assertIsNone(builder.installer)

    def test_build_correctly_resolves_dependencies(self):
        self.builder.build()

        self.assertIsNotNone(self.builder.preparation)
        self.assertIsNotNone(self.builder.installer)

    def test_build_correctly_creates_theme(self):
        self.builder.with_mode("light").filled()

        theme = self.builder.build()

        self.assertEqual(theme._preparation, self.builder.preparation)
        self.assertEqual(theme._installer, self.builder.installer)
        self.assertTrue(theme.is_filled)
        self.assertTrue(len(theme.modes) == 1)
        self.assertEqual(theme.modes[0], "light")

    def test_filled_method_with_parameter(self):
        self.builder.filled(False)
        self.assertFalse(self.builder.is_filled)

        self.builder.filled(True)
        self.assertTrue(self.builder.is_filled)