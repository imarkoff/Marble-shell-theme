import os
import shutil

from scripts.utils import copy_files


class ThemeTempManager:
    """
    Manages operations with temp folder for Theme class
    """
    def __init__(self, temp_folder: str):
        self.temp_folder = temp_folder

    def copy_to_temp(self, content: str):
        if os.path.isfile(content):
            shutil.copy(content, self.temp_folder)
        else:
            shutil.copytree(content, self.temp_folder)
        return self

    def prepare_files(self, sources_location: str):
        """Prepare files in temp folder"""
        copy_files(sources_location, self.temp_folder)

    def cleanup(self):
        """Remove temporary folders"""
        shutil.rmtree(f"{self.temp_folder}/.css/", ignore_errors=True)
        shutil.rmtree(f"{self.temp_folder}/.versions/", ignore_errors=True)