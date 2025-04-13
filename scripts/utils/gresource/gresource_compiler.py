import textwrap
from pathlib import Path

from scripts.utils.command_runner.command_runner import CommandRunner
from scripts.utils.gresource import raise_gresource_error
from scripts.utils.logger.logger import LoggerFactory


class GresourceCompiler:
    def __init__(
            self, source_folder: str, target_file: str,
            logger_factory: LoggerFactory, runner: CommandRunner
    ):
        self.source_folder = source_folder
        self.target_file = target_file
        self.gresource_xml = target_file + ".xml"

        self.logger_factory = logger_factory
        self.runner = runner

    def compile(self):
        compile_line = self.logger_factory.create_logger()
        compile_line.update("Compiling gnome-shell theme...")

        self._create_gresource_xml()
        self._compile_resources()

        compile_line.success("Compiled gnome-shell theme.")

    def _create_gresource_xml(self):
        with open(self.gresource_xml, 'w') as gresource_xml:
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
        source_path = Path(self.source_folder)
        return [
            f"<file>{file.relative_to(source_path)}</file>"
            for file in source_path.glob('**/*')
            if file.is_file()
        ]

    def _compile_resources(self):
        try:
            self._try_compile_resources()
        except FileNotFoundError as e:
            if "glib-compile-resources" in str(e):
                raise_gresource_error("glib-compile-resources", e)
            raise

    def _try_compile_resources(self):
        self.runner.run(["glib-compile-resources",
                        "--sourcedir", self.source_folder,
                        "--target", self.target_file,
                        self.gresource_xml
                        ],
                       cwd=self.source_folder, check=True)
