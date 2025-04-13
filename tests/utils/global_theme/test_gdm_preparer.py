import os
import shutil
import unittest
from unittest.mock import MagicMock, patch

from scripts import config
from scripts.types.theme_base import ThemeBase
from scripts.utils.global_theme.gdm_preparer import GDMThemePreparer


class DummyTheme(ThemeBase):
    def __init__(self):
        super().__init__()
        self.temp_folder = None
        self.main_styles = None

    def prepare(self):
        pass

    def install(self, hue: int, name: str, sat: float | None = None):
        pass


class TestGDMThemePreparer(unittest.TestCase):
    def setUp(self):
        self.temp_folder = os.path.join(config.temp_tests_folder, "gdm_preparer")

        self.gresource = self._mock_gresource(self.temp_folder)
        self.theme_builder = self._mock_builder()

        self.mock_logger = MagicMock()
        self.logger_factory = MagicMock()
        self.logger_factory.create_logger.return_value = self.mock_logger

        self.preparer = GDMThemePreparer(
            temp_folder=self.temp_folder,
            default_mode="light",
            is_filled=True,
            gresource=self.gresource,
            theme_builder=self.theme_builder,
            logger_factory=self.logger_factory,
            files_labeler_factory=MagicMock(),
        )

    @staticmethod
    def _mock_gresource(temp_folder):
        gresource = MagicMock()
        gresource.temp_folder = temp_folder
        gresource.extract = MagicMock()
        gresource.use_backup_gresource = MagicMock()
        return gresource

    @staticmethod
    def _mock_builder():
        theme_builder = MagicMock()
        theme_builder.with_temp_folder.return_value = theme_builder
        theme_builder.with_theme_name.return_value = theme_builder
        theme_builder.with_mode.return_value = theme_builder
        theme_builder.filled.return_value = theme_builder
        theme_builder.with_logger_factory.return_value = theme_builder
        theme_builder.with_reset_dependencies.return_value = theme_builder
        theme_builder.build.return_value = DummyTheme()
        return theme_builder

    def tearDown(self):
        shutil.rmtree(self.temp_folder, ignore_errors=True)

    def test_use_backup_as_source(self):
        self.preparer.use_backup_as_source()

        self.gresource.use_backup_gresource.assert_called_once()

    @patch("os.listdir")
    def test_preparer_extracts_gresource(self, mock_listdir):
        mock_listdir.return_value = ["gnome-shell.css"]

        self.preparer.prepare()

        self.gresource.extract.assert_called_once()

    @patch("os.listdir")
    def test_preparer_scans_correct_directory(self, mock_listdir):
        mock_listdir.return_value = ["gnome-shell.css"]

        self.preparer.prepare()

        mock_listdir.assert_called_once_with(self.gresource.temp_folder)

    @patch("os.listdir")
    def test_preparer_filters_valid_css_files(self, mock_listdir):
        valid_files = ["gnome-shell-dark.css", "gnome-shell-light.css", "gnome-shell.css"]
        invalid_files = ["other.css", "readme.txt"]
        mock_listdir.return_value = valid_files + invalid_files

        themes = self.preparer.prepare()

        self.assertEqual(len(themes), len(valid_files))

    @patch("os.listdir")
    def test_preparer_assigns_correct_labels(self, mock_listdir):
        test_files = ["gnome-shell-dark.css", "gnome-shell-light.css", "gnome-shell.css"]
        mock_listdir.return_value = test_files

        themes = self.preparer.prepare()

        expected_labels = {
            "gnome-shell-dark.css": "dark",
            "gnome-shell-light.css": "light",
            "gnome-shell.css": "light"  # Uses default_mode
        }

        for theme_obj in themes:
            file_name = os.path.basename(theme_obj.theme_file)
            self.assertEqual(theme_obj.label, expected_labels[file_name])

    @patch("os.listdir")
    def test_preparer_configures_theme_builder_correctly(self, mock_listdir):
        mock_listdir.return_value = ["gnome-shell-dark.css", "gnome-shell.css"]

        self.preparer.prepare()

        self.theme_builder.with_theme_name.assert_any_call("gnome-shell-dark")
        self.theme_builder.with_theme_name.assert_any_call("gnome-shell")

