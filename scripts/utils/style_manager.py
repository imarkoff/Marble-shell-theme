import os

from scripts.utils import generate_file


class StyleManager:
    """Manages the style files for the theme."""

    def __init__(self, output_file: str):
        """
        :param output_file: The path to the output file where styles will be combined.
        """
        self.output_file = output_file

    def append_content(self, content: str):
        """
        Append content to the output file.
        :raises FileNotFoundError: if the file does not exist.
        """
        if not os.path.exists(self.output_file):
            raise FileNotFoundError(f"The file {self.output_file} does not exist.")
        with open(self.output_file, 'a') as output:
            output.write('\n' + content)

    def prepend_content(self, content: str):
        """
        Prepend content to the output file.
        :raises FileNotFoundError: if the file does not exist.
        """
        with open(self.output_file, 'r') as output:
            main_content = output.read()
        with open(self.output_file, 'w') as output:
            output.write(content + '\n' + main_content)

    def generate_combined_styles(self, sources_location: str, temp_folder: str):
        """
        Generate the combined styles file
        by merging all styles from the source location.
        """
        generate_file(sources_location, temp_folder, self.output_file)