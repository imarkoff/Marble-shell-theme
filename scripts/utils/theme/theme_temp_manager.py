import os
import shutil


class ThemeTempManager:
    """
    Manages operations with temp folder for Theme class
    """
    def __init__(self, temp_folder: str):
        self.temp_folder = temp_folder
        os.makedirs(self.temp_folder, exist_ok=True)

    def copy_to_temp(self, content: str):
        """
        Copy a file or directory to the temporary folder.
        If the content is a file, it will be copied directly.
        If the content is a directory, all its contents will be copied to the temp folder.
        """
        if os.path.isfile(content):
            final_path = os.path.join(self.temp_folder, os.path.basename(content))
            shutil.copy(content, final_path)
        else:
            shutil.copytree(content, self.temp_folder, dirs_exist_ok=True)
        return self

    def cleanup(self):
        """Remove temporary folders"""
        shutil.rmtree(f"{self.temp_folder}/.css/", ignore_errors=True)
        shutil.rmtree(f"{self.temp_folder}/.versions/", ignore_errors=True)