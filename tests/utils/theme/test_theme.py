import os.path
import unittest
from unittest.mock import MagicMock

from scripts import config
from scripts.types.installation_color import InstallationColor
from scripts.utils.theme.theme import Theme


class ThemeTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_preparation = MagicMock()
        self.mock_installer = MagicMock()

        temp_folder = os.path.join(config.temp_tests_folder, "theme_temp")
        destination_folder = os.path.join(temp_folder, "theme_destination")

        self.mock_preparation.temp_folder = temp_folder
        self.mock_preparation.combined_styles_location = os.path.join(temp_folder, "styles.css")
        self.mock_installer.destination_folder = destination_folder
        self.mock_installer.theme_type = "gtk"

        self.theme = Theme(self.mock_preparation, self.mock_installer)

    def test_default_initialization_works_correctly(self):
        self.assertEqual(self.theme.modes, ['light', 'dark'])
        self.assertFalse(self.theme.is_filled)

    def test_initialization_with_specific_mode_works_correctly(self):
        theme_light = Theme(self.mock_preparation, self.mock_installer, mode='light')
        self.assertEqual(theme_light.modes, ['light'])

    def test_initialization_with_is_filled_works_correctly(self):
        theme_filled = Theme(self.mock_preparation, self.mock_installer, is_filled=True)
        self.assertTrue(theme_filled.is_filled)

    def test_properties_fetch_values_correctly(self):
        temp_folder = os.path.join(config.temp_tests_folder, "theme_temp")
        destination_folder = os.path.join(temp_folder, "theme_destination")

        self.assertEqual(self.theme.temp_folder, temp_folder)
        self.assertEqual(self.theme.destination_folder, destination_folder)
        self.assertEqual(self.theme.main_styles, os.path.join(temp_folder, "styles.css"))
        self.assertEqual(self.theme.theme_name, "gtk")

    def test_add_operator_called_once_and_return_value(self):
        result = self.theme + "additional styles"

        self.mock_preparation.__iadd__.assert_called_once_with("additional styles")
        self.assertEqual(result, self.theme)

    def test_mul_operator_called_once_and_return_value(self):
        result = self.theme * "/path/to/file"

        self.mock_preparation.__imul__.assert_called_once_with("/path/to/file")
        self.assertEqual(result, self.theme)

    def test_add_to_start_called_once_and_return_value(self):
        result = self.theme.add_to_start("starting content")

        self.mock_preparation.add_to_start.assert_called_once_with("starting content")
        self.assertEqual(result, self.theme)

    def test_prepare_called_once(self):
        self.theme.prepare()

        self.mock_preparation.prepare.assert_called_once()

    def test_install_without_optional_params_called_correctly(self):
        self.theme.install(200, "Green")

        args = self.mock_installer.install.call_args[0]
        self.assertEqual(args[0].hue, 200)
        self.assertIsNone(args[0].saturation)
        self.assertEqual(args[1], "Green")
        self.assertIsNone(args[2])

    def test_install_with_optional_params_called_correctly(self):
        self.theme.install(hue=180, name="Blue", sat=0.5, destination="/custom/dest")

        self.mock_installer.install.assert_called_once()
        args = self.mock_installer.install.call_args[0]

        theme_color = args[0]
        self.assertIsInstance(theme_color, InstallationColor)
        self.assertEqual(theme_color.hue, 180)
        self.assertEqual(theme_color.saturation, 0.5)
        self.assertEqual(theme_color.modes, ['light', 'dark'])
        self.assertEqual(args[1], "Blue")
        self.assertEqual(args[2], "/custom/dest")
