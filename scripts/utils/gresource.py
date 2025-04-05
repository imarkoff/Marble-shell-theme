import os
import subprocess
import textwrap
from pathlib import Path

from scripts.utils.console import Console


class GresourceBackupNotFoundError(FileNotFoundError):
    def __init__(self, location: str = None):
        if location:
            super().__init__(f"Gresource backup file not found: {location}")
        else:
            super().__init__("Gresource backup file not found.")

class MissingDependencyError(Exception):
    def __init__(self, dependency: str):
        super().__init__(f"Missing required dependency: {dependency}")
        self.dependency = dependency


class Gresource:
    """Handles the extraction and compilation of gresource files for GNOME Shell themes."""

    def __init__(self, gresource_file: str, temp_folder: str, destination: str):
        """
        :param gresource_file: The name of the gresource file to be processed.
        :param temp_folder: The temporary folder where resources will be extracted.
        :param destination: The destination folder where the compiled gresource file will be saved.
        """
        self.gresource_file = gresource_file
        self.temp_folder = temp_folder
        self.destination = destination

        self._temp_gresource = os.path.join(temp_folder, gresource_file)
        self._destination_gresource = os.path.join(destination, gresource_file)
        self._active_source_gresource = self._destination_gresource
        self._backup_gresource = os.path.join(destination, f"{gresource_file}.backup")
        self._gresource_xml = os.path.join(temp_folder, f"{gresource_file}.xml")

    def use_backup_gresource(self):
        if not os.path.exists(self._backup_gresource):
            raise GresourceBackupNotFoundError(self._backup_gresource)
        self._active_source_gresource = self._backup_gresource

    def extract(self):
        extract_line = Console.Line()
        extract_line.update("Extracting gresource files...")

        resources = self._get_resources_list()
        self._extract_resources(resources)

        extract_line.success("Extracted gresource files.")

    def _get_resources_list(self):
        resources_list_response = subprocess.run(
            ["gresource", "list", self._active_source_gresource],
            capture_output=True, text=True, check=False
        )

        if resources_list_response.stderr:
            raise Exception(f"gresource could not process the theme file: {self._active_source_gresource}")

        return resources_list_response.stdout.strip().split("\n")

    def _extract_resources(self, resources: list[str]):
        prefix = "/org/gnome/shell/theme/"
        try:
            for resource in resources:
                resource_path = resource.replace(prefix, "")
                output_path = os.path.join(self.temp_folder, resource_path)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                with open(output_path, 'wb') as f:
                    subprocess.run(
                        ["gresource", "extract", self._active_source_gresource, resource],
                        stdout=f, check=True
                    )
        except FileNotFoundError as e:
            if "gresource" in str(e):
                self._raise_gresource_error(e)
            raise

    @staticmethod
    def _raise_gresource_error(e: Exception):
        print("Error: 'gresource' command not found.")
        print("Please install the glib2-devel package:")
        print(" - For Fedora/RHEL: sudo dnf install glib2-devel")
        print(" - For Ubuntu/Debian: sudo apt install libglib2.0-dev")
        print(" - For Arch: sudo pacman -S glib2-devel")
        raise MissingDependencyError("glib2-devel") from e

    def compile(self):
        compile_line = Console.Line()
        compile_line.update("Compiling gnome-shell theme...")

        self._create_gresource_xml()
        self._compile_resources()

        compile_line.success("Theme compiled.")

    def _create_gresource_xml(self):
        with open(self._gresource_xml, 'w') as gresource_xml:
            gresource_xml.write(self._generate_gresource_xml())

    def _generate_gresource_xml(self):
        files_to_include = self._get_files_to_include()
        nl = "\n"  # fstring doesn't support newline character
        return textwrap.dedent(f"""
            <?xml version="1.0" encoding="UTF-8"?>
            <gresources>
                <gresource prefix="/org/gnome/shell/theme">
                    {nl.join(files_to_include)}
                </gresource>
            </gresources>
        """)

    def _get_files_to_include(self):
        temp_path = Path(self.temp_folder)
        return [
            f"<file>{file.relative_to(temp_path)}</file>"
            for file in temp_path.glob('**/*')
            if file.is_file()
        ]

    def _compile_resources(self):
        try:
            subprocess.run(["glib-compile-resources",
                            "--sourcedir", self.temp_folder,
                            "--target", self._temp_gresource,
                            self._gresource_xml
                            ],
                           cwd=self.temp_folder, check=True)
        except FileNotFoundError as e:
            if "glib-compile-resources" in str(e):
                self._raise_gresource_error(e)
            raise

    def backup(self):
        backup_line = Console.Line()
        backup_line.update("Backing up gresource files...")

        subprocess.run(["cp", "-aT",
                        self._destination_gresource,
                        self._backup_gresource],
                       check=True)

        backup_line.success("Backed up gresource files.")

    def restore(self):
        if not os.path.exists(self._backup_gresource):
            raise GresourceBackupNotFoundError(self._backup_gresource)

        subprocess.run(["mv", "-f",
                        self._backup_gresource,
                        self._destination_gresource],
                       check=True)


    def move(self):
        move_line = Console.Line()
        move_line.update("Moving gresource files...")

        subprocess.run(["cp", "-f",
                        self._temp_gresource,
                        self._destination_gresource],
                       check=True)

        subprocess.run(["chmod", "644", self._destination_gresource], check=True)

        move_line.success("Moved gresource files.")