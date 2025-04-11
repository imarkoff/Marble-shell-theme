import unittest

from scripts.utils.color_converter.color_converter_impl import ColorConverterImpl


class ColorConverterImplTestCase(unittest.TestCase):
    def setUp(self):
        self.converter = ColorConverterImpl()

    def test_hex_to_rgba_is_valid(self):
        hex_color = "#ff5733"
        expected_rgba = (255, 87, 51, 1.0)

        result = self.converter.hex_to_rgba(hex_color)

        self.assertEqual(result, expected_rgba)

    def test_hex_to_rgba_is_invalid(self):
        hex_color = "#invalid"

        with self.assertRaises(ValueError):
            self.converter.hex_to_rgba(hex_color)

    def test_hex_to_rgba_with_alpha_is_valid(self):
        hex_color = "#ff5733ff"
        expected_rgba = (255, 87, 51, 1.0)

        result = self.converter.hex_to_rgba(hex_color)

        self.assertEqual(result, expected_rgba)

    def test_hex_to_rgba_with_shorthand_is_valid(self):
        hex_color = "#fff"
        expected_rgba = (255, 255, 255, 1.0)

        result = self.converter.hex_to_rgba(hex_color)

        self.assertEqual(result, expected_rgba)

    def test_hsl_to_rgb_is_valid(self):
        hue = 360
        saturation = 1
        lightness = 0.5
        expected_rgb = (255, 0, 0)

        result = self.converter.hsl_to_rgb(hue, saturation, lightness)

        self.assertEqual(result, expected_rgb)

    def test_hsl_to_rgb_with_overflow_hue_is_invalid(self):
        hue = 400
        saturation = 1
        lightness = 0.5

        with self.assertRaises(ValueError):
            self.converter.hsl_to_rgb(hue, saturation, lightness)

    def test_hsl_to_rgb_with_invalid_saturation_and_lightness_is_invalid(self):
        hue = 360
        saturation = 1.5
        lightness = -2

        with self.assertRaises(ValueError):
            self.converter.hsl_to_rgb(hue, saturation, lightness)