import os

from scripts.types.installation_color import InstallationColor, InstallationMode
from scripts.utils import replace_keywords
from scripts.utils.theme.color_replacement_generator import ColorReplacementGenerator


class ThemeColorApplier:
    """Class to apply theme colors to files in a directory."""

    def __init__(self, color_replacement_generator: ColorReplacementGenerator):
        self.color_replacement_generator = color_replacement_generator

    def apply(self, theme_color: InstallationColor, destination: str, mode: InstallationMode):
        """Apply theme colors to all files in the directory"""
        replacements = self.color_replacement_generator.convert(mode, theme_color)

        for filename in os.listdir(destination):
            file_path = os.path.join(destination, filename)
            replace_keywords(file_path, *replacements)
