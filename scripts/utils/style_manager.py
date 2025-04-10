from scripts.utils import generate_file


class StyleManager:
    def __init__(self, output_file: str):
        self.output_file = output_file

    def append_content(self, content: str):
        with open(self.output_file, 'a') as output:
            output.write(content + '\n')

    def prepend_content(self, content: str):
        with open(self.output_file, 'r') as output:
            main_content = output.read()
        with open(self.output_file, 'w') as output:
            output.write(content + '\n' + main_content)

    def generate_combined_styles(self, sources_location: str, temp_folder: str):
        generate_file(sources_location, temp_folder, self.output_file)