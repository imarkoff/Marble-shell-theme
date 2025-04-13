import os
from abc import ABC, abstractmethod
from typing import Tuple, TypeAlias

LabeledFileGroup: TypeAlias = Tuple[str, str]


class FilesLabelerFactory(ABC):
    @abstractmethod
    def create(self, temp_folder: str, *files_to_update_references: str) -> 'FilesLabeler':
        pass


class FilesLabelerFactoryImpl(FilesLabelerFactory):
    def create(self, temp_folder: str, *files_to_update_references: str) -> 'FilesLabeler':
        return FilesLabeler(temp_folder, *files_to_update_references)


class FilesLabeler:
    def __init__(self, directory: str, *files_to_update_references: str):
        """
        Initialize the working directory and files to change
        """
        self.directory = directory
        self.files = files_to_update_references

    def append_label(self, label: str):
        """
        Append a label to all files in the directory
        and update references in the files
        """
        labeled_files = self._label_files(label)
        self._update_references(labeled_files)

    def _label_files(self, label: str) -> list[LabeledFileGroup]:
        labeled_files = []
        for filename in os.listdir(self.directory):
            if label in filename: continue

            name, extension = os.path.splitext(filename)
            new_filename = f"{name}-{label}{extension}"

            old_filepath = os.path.join(self.directory, filename)
            new_filepath = os.path.join(self.directory, new_filename)
            os.rename(old_filepath, new_filepath)

            labeled_files.append((filename, new_filename))
        return labeled_files

    def _update_references(self, labeled_files: list[LabeledFileGroup]):
        for file_path in self.files:
            with open(file_path, 'r') as file:
                file_content = file.read()

            file_content = self._update_references_in_file(file_content, labeled_files)

            with open(file_path, 'w') as file:
                file.write(file_content)

    @staticmethod
    def _update_references_in_file(file_content: str, labeled_files: list[LabeledFileGroup]) -> str:
        replaced_content = file_content
        for old_name, new_name in labeled_files:
            replaced_content = replaced_content.replace(old_name, new_name)
        return replaced_content