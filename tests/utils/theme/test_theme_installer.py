import os
import shutil
import unittest
from unittest.mock import Mock

from scripts import config
from scripts.utils.theme.theme_installer import ThemeInstaller
from scripts.utils.theme.theme_path_provider import ThemePathProvider
from ..._helpers import create_dummy_file


class ThemeInstallerTestCase(unittest.TestCase):
    def setUp(self):
        self.theme_type = "gnome-shell"
        self.source_folder = os.path.join(config.temp_tests_folder, "theme_installer_source")
        self.destination_folder = os.path.join(config.temp_tests_folder, "theme_installer_destination")
        self.custom_destination_folder = os.path.join(config.temp_tests_folder, "theme_installer_custom_destination")

        self.logger_factory = Mock()
        self.color_applier = Mock()
        self.path_provider = ThemePathProvider()
        self.path_provider.get_theme_path = Mock(return_value=self.destination_folder)

        self.theme_installer = ThemeInstaller(
            theme_type=self.theme_type,
            source_folder=self.source_folder,
            destination_folder=self.destination_folder,
            logger_factory=self.logger_factory,
            color_applier=self.color_applier,
            path_provider=self.path_provider,
        )

        self._setup_source_folder()

    def tearDown(self):
        shutil.rmtree(self.source_folder, ignore_errors=True)
        shutil.rmtree(self.destination_folder, ignore_errors=True)
        shutil.rmtree(self.custom_destination_folder, ignore_errors=True)

    def _setup_source_folder(self):
        os.makedirs(self.source_folder, exist_ok=True)
        first_file = os.path.join(self.source_folder, "file1.css")
        second_file = os.path.join(self.source_folder, "file2.css")
        first_css = "body { background-color: ACCENT-COLOR; color: ACCENT_HOVER; }"
        second_css = "body { background-color: BACKGROUND-COLOR; }"
        create_dummy_file(first_file, first_css)
        create_dummy_file(second_file, second_css)

    def test_install_calls_get_theme_path_and_apply_methods_with_correct_parameters(self):
        theme_color = Mock()
        theme_color.modes = ["light"]
        name = "test-theme"

        self.theme_installer.install(theme_color, name)

        # noinspection PyUnresolvedReferences
        self.path_provider.get_theme_path.assert_called_once_with(
            self.destination_folder, name, "light", self.theme_type
        )
        self.color_applier.apply.assert_called_once_with(theme_color, self.destination_folder, "light")

    def test_install_with_custom_destination_calls_get_theme_path_and_apply_methods_with_correct_parameters(self):
        theme_color = Mock()
        theme_color.modes = ["light"]
        name = "test-theme"
        os.makedirs(self.custom_destination_folder, exist_ok=True)

        self.theme_installer.install(theme_color, name, self.custom_destination_folder)

        # noinspection PyUnresolvedReferences
        self.path_provider.get_theme_path.assert_not_called()
        self.color_applier.apply.assert_called_once_with(theme_color, self.custom_destination_folder, "light")

    def test_install_with_multiple_modes_calls_get_theme_path_and_apply_methods_for_each_mode(self):
        theme_color = Mock()
        theme_color.modes = ["light", "dark"]
        name = "test-theme"

        self.theme_installer.install(theme_color, name)

        # noinspection PyUnresolvedReferences
        self.assertEqual(self.path_provider.get_theme_path.call_count, 2)
        self.assertEqual(self.color_applier.apply.call_count, 2)

    def test_install_raises_exception_and_logs_error(self):
        theme_color = Mock()
        theme_color.modes = ["light"]
        name = "test-theme"
        self.color_applier.apply.side_effect = Exception("Test error")

        with self.assertRaises(Exception):
            self.theme_installer.install(theme_color, name)

        logger_mock = self.logger_factory.create_logger.return_value
        self.assertTrue(logger_mock.error.called)

    def test_install_copies_files_to_destination(self):
        theme_color = Mock()
        theme_color.modes = ["light"]
        name = "test-theme"
        destination = os.path.join(self.destination_folder, "actual_destination")
        self.path_provider.get_theme_path.return_value = destination

        self.theme_installer.install(theme_color, name)

        first_file_exists = os.path.exists(os.path.join(destination, "file1.css"))
        second_file_exists = os.path.exists(os.path.join(destination, "file2.css"))
        self.assertTrue(first_file_exists)
        self.assertTrue(second_file_exists)