import os

from scripts.utils.command_runner.command_runner import CommandRunner
from scripts.utils.gresource import raise_gresource_error
from scripts.utils.logger.logger import LoggerFactory


class GresourceExtractor:
    def __init__(
            self, gresource_path: str, extract_folder: str,
            logger_factory: LoggerFactory, runner: CommandRunner
    ):
        self.gresource_path = gresource_path
        self.extract_folder = extract_folder
        self.logger_factory = logger_factory
        self.runner = runner

    def extract(self):
        extract_line = self.logger_factory.create_logger()
        extract_line.update("Extracting gresource files...")

        self._try_extract_resources()

        extract_line.success("Extracted gresource files.")

    def _try_extract_resources(self):
        try:
            resources = self._get_resources_list()
            self._extract_resources(resources)
        except FileNotFoundError as e:
            print(e)
            if "gresource" in str(e):
                raise_gresource_error("gresource", e)
            raise
        except Exception as e:
            raise Exception(f"gresource could not process the theme file: {self.gresource_path}") from e

    def _get_resources_list(self):
        resources_list_response = self.runner.run(
            ["gresource", "list", self.gresource_path],
            capture_output=True, text=True, check=True
        )
        return resources_list_response.stdout.strip().split("\n")

    def _extract_resources(self, resources: list[str]):
        prefix = "/org/gnome/shell/theme/"
        for resource in resources:
            resource_path = resource.replace(prefix, "")
            output_path = os.path.join(self.extract_folder, resource_path)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            with open(output_path, 'wb') as f:
                self.runner.run(
                    ["gresource", "extract", self.gresource_path, resource],
                    stdout=f, check=True
                )
