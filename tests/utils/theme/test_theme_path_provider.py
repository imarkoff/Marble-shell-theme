import unittest

from scripts.utils.theme.theme_path_provider import ThemePathProvider


class ThemePathProviderTestCase(unittest.TestCase):
    def setUp(self):
        self.theme_path_provider = ThemePathProvider()

    def test_get_theme_path_with_valid_values_returns_correct_path(self):
        themes_folder = "/usr/share/themes"
        color_name = "Marble"
        theme_mode = "dark"
        theme_type = "gnome-shell"

        expected_path = f"{themes_folder}/Marble-{color_name}-{theme_mode}/{theme_type}/"
        actual_path = self.theme_path_provider.get_theme_path(themes_folder, color_name, theme_mode, theme_type)

        assert expected_path == actual_path

    def test_get_theme_path_with_empty_values_raises_exception(self):
        themes_folder = ""
        color_name = ""
        theme_mode = ""
        theme_type = ""

        with self.assertRaises(ValueError):
            self.theme_path_provider.get_theme_path(themes_folder, color_name, theme_mode, theme_type)