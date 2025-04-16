import os

from scripts.utils import replace_keywords
from scripts.utils.theme.theme_temp_manager import ThemeTempManager
from scripts.utils.style_manager import StyleManager


class ThemePreparation:
    """
    Class for extracting themes from the source folder
    and preparing them for installation.
    """

    def __init__(self, sources_location: str, file_manager: ThemeTempManager, style_manager: StyleManager):
        self.sources_location = sources_location

        self.file_manager = file_manager
        self.style_manager = style_manager

    @property
    def temp_folder(self):
        return self.file_manager.temp_folder

    @property
    def combined_styles_location(self):
        return self.style_manager.output_file

    def __add__(self, content: str) -> "ThemePreparation":
        """Append additional styles to the main styles file."""
        self.style_manager.append_content(content)
        return self

    def __mul__(self, content: str) -> "ThemePreparation":
        """Adds a file to the theme, copying it to the temporary folder."""
        self.file_manager.copy_to_temp(content)
        return self

    def add_to_start(self, content) -> "ThemePreparation":
        """Inserts content at the beginning of the main styles file."""
        self.style_manager.prepend_content(content)
        return self

    def add_from_file(self, content) -> "ThemePreparation":
        """
        Adds content from a file to the main styles file.
        :param content: The path of the file to add.
        """
        with open(content, "r") as f:
            self.style_manager.append_content(f.read())
        return self

    def prepare(self):
        """
        Extract theme from source folder and prepare it for installation.
        """
        self.file_manager.copy_to_temp(self.sources_location)
        self.style_manager.generate_combined_styles(self.sources_location, self.temp_folder)
        self.file_manager.cleanup()

    def replace_filled_keywords(self):
        """
        Replace keywords in the theme files for filled mode.
        This method is deprecated and will be removed in future versions.
        """
        for apply_file in os.listdir(f"{self.temp_folder}/"):
            replace_keywords(f"{self.temp_folder}/{apply_file}",
                             ("BUTTON-COLOR", "ACCENT-FILLED-COLOR"),
                             ("BUTTON_HOVER", "ACCENT-FILLED_HOVER"),
                             ("BUTTON_ACTIVE", "ACCENT-FILLED_ACTIVE"),
                             ("BUTTON_INSENSITIVE", "ACCENT-FILLED_INSENSITIVE"),
                             ("BUTTON-TEXT-COLOR", "TEXT-BLACK-COLOR"),
                             ("BUTTON-TEXT_SECONDARY", "TEXT-BLACK_SECONDARY"))
