import copy
import os

from scripts.install.colors_definer import ColorsDefiner
from scripts.types.installation_color import InstallationColor, InstallationMode
from scripts.utils import replace_keywords
from scripts.utils.color_converter import ColorConverter


class ThemeColorApplier:
    """Class to apply theme colors to files in a directory."""

    def __init__(self, color_replacement_generator: "ColorReplacementGenerator"):
        self.color_replacement_generator = color_replacement_generator

    def apply(self, theme_color: InstallationColor, destination: str, mode: InstallationMode):
        """Apply theme colors to all files in the directory"""
        replacements = self.color_replacement_generator.convert(mode, theme_color)

        for filename in os.listdir(destination):
            file_path = os.path.join(destination, filename)
            replace_keywords(file_path, *replacements)


class ColorReplacementGenerator:
    def __init__(self, colors_provider: ColorsDefiner, color_converter: ColorConverter):
        self.colors = copy.deepcopy(colors_provider)
        self.color_converter = color_converter

    def convert(self, mode: InstallationMode, theme_color: InstallationColor) -> list[tuple[str, str]]:
        """Generate a list of color replacements for the given theme color and mode"""
        return [
            (element, self._create_rgba_value(element, mode, theme_color))
            for element in self.colors.replacers
        ]

    def _create_rgba_value(self, element: str, mode: str, theme_color: InstallationColor) -> str:
        """Create RGBA value for the specified element"""
        color_def = self._get_color_definition(element, mode)

        lightness = int(color_def["l"]) / 100
        saturation = int(color_def["s"]) / 100
        if theme_color.saturation is not None:
            saturation *= theme_color.saturation / 100
        alpha = color_def["a"]

        red, green, blue = self.color_converter.hsl_to_rgb(
            theme_color.hue, saturation, lightness
        )

        return f"rgba({red}, {green}, {blue}, {alpha})"

    def _get_color_definition(self, element: str, mode: str) -> dict:
        """Get color definition for element, handling defaults if needed"""
        replacer = self.colors.replacers[element]

        if mode not in replacer and replacer["default"]:
            default_element = replacer["default"]
            return self.colors.replacers[default_element][mode]

        return replacer[mode]