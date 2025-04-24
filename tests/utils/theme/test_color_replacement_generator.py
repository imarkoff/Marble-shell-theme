import os.path
import unittest

from scripts.install.colors_definer import ColorsDefiner
from scripts.types.installation_color import InstallationColor, InstallationMode
from scripts.utils.color_converter.color_converter_impl import ColorConverterImpl
from scripts.utils.theme.color_replacement_generator import ColorReplacementGenerator

class ColorReplacementGeneratorTestCase(unittest.TestCase):
    def setUp(self):
        colors_location = os.path.join(os.path.dirname(__file__), "assets", "colors.json")
        self.colors_provider = ColorsDefiner(colors_location)
        self.color_converter = ColorConverterImpl()
        self.generator = ColorReplacementGenerator(self.colors_provider, self.color_converter)

    def test_convert_red_color_in_dark_mode_generates_correct_rgba(self):
        theme_color = InstallationColor(hue=0, saturation=None, modes=[])
        mode: InstallationMode = "dark"
        expected_output = self._get_expected_output(theme_color, mode)

        actual_output = self.generator.convert(mode, theme_color)

        self._assert_expected_and_actual_replacers_match(expected_output, actual_output)

    def test_convert_gray_color_in_light_mode_generates_correct_rgba(self):
        theme_color = InstallationColor(hue=0, saturation=0, modes=[])
        mode: InstallationMode = "light"
        expected_output = self._get_expected_output(theme_color, mode)

        actual_output = self.generator.convert(mode, theme_color)

        self._assert_expected_and_actual_replacers_match(expected_output, actual_output)

    def test_convert_not_existent_mode_raises_key_error(self):
        theme_color = InstallationColor(hue=0, saturation=0, modes=[])
        mode = "not_existent_mode"

        with self.assertRaises(KeyError):
            # noinspection PyTypeChecker
            self.generator.convert(mode, theme_color)

    def _get_expected_output(self, theme_color: InstallationColor, mode: str):
        return [
            ("ACCENT-COLOR", self._get_rgba("ACCENT-COLOR", theme_color, mode)),
            ("ACCENT_HOVER", self._get_rgba("ACCENT_HOVER", theme_color, mode)),
            ("BUTTON-COLOR", self._get_rgba("BUTTON-COLOR", theme_color, mode)),
        ]

    def _get_rgba(self, replacer_name: str, theme_color: InstallationColor, mode: str):
        expected_colors: dict = self.colors_provider.colors.get("expected")
        replacer_colors = expected_colors.get(replacer_name)
        saturation = theme_color.saturation if theme_color.saturation is not None else 100
        variant_colors = replacer_colors.get(f"{theme_color.hue},{saturation}")
        expected_rgba = variant_colors.get(mode)
        return expected_rgba

    @staticmethod
    def _assert_expected_and_actual_replacers_match(expected: list, actual: list):
        for expected_element, expected_rgba in expected:
            actual_rgba = next(
                (rgba for element, rgba in actual if element == expected_element), None
            )
            assert actual_rgba is not None
            assert expected_rgba == actual_rgba

    def test_convert_with_saturation_higher_than_100_should_round_to_max_value_on_overflow(self):
        theme_color = InstallationColor(hue=0, saturation=999, modes=[])
        mode: InstallationMode = "dark"
        expected_output = self._get_expected_output(theme_color, mode)

        actual_output = self.generator.convert(mode, theme_color)

        self.assertEqual(len(expected_output), len(actual_output))
        for expected_name, expected_value in expected_output:
            actual_value = next(
                (value for name, value in actual_output if name == expected_name), None
            )
            self.assertIsNotNone(actual_value)
            self.assertEqual(expected_value, actual_value)