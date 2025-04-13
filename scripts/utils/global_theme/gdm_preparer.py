import os

from scripts.utils.files_labeler import FilesLabelerFactory
from scripts.utils.global_theme.gdm_theme_prepare import GDMThemePrepare
from scripts.utils.gresource.gresource import Gresource
from scripts.utils.logger.logger import LoggerFactory
from scripts.utils.theme.gnome_shell_theme_builder import GnomeShellThemeBuilder


class GDMThemePreparer:
    """
    GDM theme preparation module.

    This module contains classes responsible for extracting and processing
    GDM theme resources for later compilation and installation.

    The main class, GDMThemePreparer, orchestrates the extraction process
    and creates GDMThemePrepare objects representing processable themes.
    """
    def __init__(self, temp_folder: str, default_mode: str | None, is_filled: bool,
                 gresource: Gresource,
                 theme_builder: GnomeShellThemeBuilder,
                 logger_factory: LoggerFactory,
                 files_labeler_factory: FilesLabelerFactory):
        """
        :param temp_folder: Temporary folder for extracted theme files
        :param default_mode: Default theme mode to use if not specified in CSS filename
        :param is_filled: Whether to generate filled (True) or dimmed (False) styles
        :param gresource: Gresource instance for managing gresource files
        :param theme_builder: Theme builder instance for creating themes
        :param logger_factory: Logger factory for logging messages
        :param files_labeler_factory: Factory for creating FilesLabeler instances
        """
        self.temp_folder = temp_folder
        self.gresource_temp_folder = gresource.temp_folder

        self.default_mode = default_mode
        self.is_filled = is_filled

        self.gresource = gresource
        self.theme_builder = theme_builder
        self.logger_factory = logger_factory
        self.files_labeler_factory = files_labeler_factory

    def use_backup_as_source(self):
        """Use backup gresource file for extraction"""
        self.gresource.use_backup_gresource()
        self.logger_factory.create_logger().info("Using backup gresource file for extraction...")

    def prepare(self) -> list[GDMThemePrepare]:
        """
        Extract and prepare GDM themes for processing.
        :return: List of prepared theme objects ready for compilation
        """
        self.gresource.extract()
        return self._find_themes()

    def _find_themes(self) -> list[GDMThemePrepare]:
        extracted_files = os.listdir(self.gresource_temp_folder)
        allowed_css = {"gnome-shell-dark.css", "gnome-shell-light.css", "gnome-shell.css"}

        themes = [
            self._create_theme(file_name)
            for file_name in extracted_files
            if file_name in allowed_css
        ]
        return themes

    def _create_theme(self, file_name: str) -> GDMThemePrepare:
        """Helper to create and prepare a theme"""
        mode = file_name.split("-")[-1].replace(".css", "")
        mode = mode if mode in {"dark", "light"} else self.default_mode

        self._setup_theme_builder(file_name, mode)

        theme = self.theme_builder.build()
        theme.prepare()

        theme_file = os.path.join(self.gresource_temp_folder, file_name)
        files_labeler = self.files_labeler_factory.create(
            theme.temp_folder, theme.main_styles)
        return GDMThemePrepare(
            theme=theme, theme_file=theme_file, label=mode, files_labeler=files_labeler)

    def _setup_theme_builder(self, file_name: str, mode: str):
        theme_name = file_name.replace(".css", "")

        (self.theme_builder
         .with_temp_folder(self.temp_folder)
         .with_theme_name(theme_name)
         .with_mode(mode)
         .filled(self.is_filled)
         .with_logger_factory(self.logger_factory)
         .with_reset_dependencies())