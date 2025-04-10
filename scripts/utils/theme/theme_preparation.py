import os

from scripts.utils import replace_keywords
from scripts.utils.theme.theme_temp_manager import ThemeTempManager
from scripts.utils.style_manager import StyleManager


class ThemePreparation:
    """
    Class for extracting themes from the source folder
    and preparing them for installation.
    """

    def __init__(self, sources_location: str, temp_folder: str, combined_styles_location: str):
        self.sources_location = sources_location
        self.temp_folder = temp_folder
        self.combined_styles_location = combined_styles_location

        self.file_manager = ThemeTempManager(temp_folder)
        self.style_manager = StyleManager(combined_styles_location)

    def __add__(self, content: str) -> "ThemePreparation":
        self.style_manager.append_content(content)
        return self

    def __mul__(self, content: str) -> "ThemePreparation":
        self.file_manager.copy_to_temp(content)
        return self

    def add_to_start(self, content) -> "ThemePreparation":
        self.style_manager.prepend_content(content)
        return self

    def prepare(self):
        self.file_manager.prepare_files(self.sources_location)
        self.style_manager.generate_combined_styles(self.sources_location, self.temp_folder)
        self.file_manager.cleanup()

    def replace_filled_keywords(self):
        for apply_file in os.listdir(f"{self.temp_folder}/"):
            replace_keywords(f"{self.temp_folder}/{apply_file}",
                             ("BUTTON-COLOR", "ACCENT-FILLED-COLOR"),
                             ("BUTTON_HOVER", "ACCENT-FILLED_HOVER"),
                             ("BUTTON_ACTIVE", "ACCENT-FILLED_ACTIVE"),
                             ("BUTTON_INSENSITIVE", "ACCENT-FILLED_INSENSITIVE"),
                             ("BUTTON-TEXT-COLOR", "TEXT-BLACK-COLOR"),
                             ("BUTTON-TEXT_SECONDARY", "TEXT-BLACK_SECONDARY"))