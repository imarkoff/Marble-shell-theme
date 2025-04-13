import os.path
from unittest import TestCase
from unittest.mock import MagicMock

from scripts import config
from scripts.utils.global_theme.gdm_installer import GDMThemeInstaller


class GDMInstallerTestCase(TestCase):
    def setUp(self):
        self.temp_folder = os.path.join(config.temp_tests_folder, "gdm_installer")
        self.gresource = MagicMock()
        self.gresource.temp_folder = self.temp_folder

        self.alternatives_updater = MagicMock()

        self.gdm_installer = GDMThemeInstaller(
            gresource=self.gresource,
            alternatives_updater=self.alternatives_updater
        )

    def test_is_installed_return_the_same_value_as_gresource(self):
        self.gresource.has_trigger.return_value = True

        result = self.gdm_installer.is_installed()

        self.assertTrue(result)
        self.gresource.has_trigger.assert_called_once()

    def test_compile_does_not_call_label_theme_if_label_is_none(self):
        theme_prepare = MagicMock()
        theme_prepare.label = None
        theme_prepare.label_theme = MagicMock()

        self.gdm_installer.compile(themes=[theme_prepare], hue=0, color="red", sat=None)

        theme_prepare.label_theme.assert_not_called()

    def test_compile_calls_label_theme_if_label_is_set(self):
        theme_prepare = MagicMock()
        theme_prepare.label = "dark"
        theme_prepare.label_theme = MagicMock()

        self.gdm_installer.compile(themes=[theme_prepare], hue=0, color="red", sat=None)

        theme_prepare.label_theme.assert_called_once()

    def test_compile_calls_removes_keywords_and_properties_and_prepends_source_styles(self):
        theme_prepare = MagicMock()
        theme_prepare.remove_keywords = MagicMock()
        theme_prepare.remove_properties = MagicMock()
        theme_prepare.prepend_source_styles = MagicMock()

        self.gdm_installer.compile(themes=[theme_prepare], hue=0, color="red", sat=None)

        theme_prepare.remove_keywords.assert_called_once()
        theme_prepare.remove_properties.assert_called_once()
        theme_prepare.prepend_source_styles.assert_called_once()

    def test_compile_installs_themes_with_correct_parameters(self):
        theme_prepare = MagicMock()
        theme_prepare.install = MagicMock()
        themes = [theme_prepare]
        hue = 0
        color = "red"
        sat = None

        self.gdm_installer.compile(themes, hue, color, sat)

        theme_prepare.install.assert_called_once()
        theme_prepare.install.assert_called_with(hue, color, sat, destination=self.temp_folder)

    def test_compile_calls_gresource_compile(self):
        self.gdm_installer.compile([], 0, "red", None)

        self.gresource.compile.assert_called_once()

    def test_backup_calls_gresource_backup(self):
        self.gdm_installer.backup()

        self.gresource.backup.assert_called_once()

    def test_install_calls_gresource_move_and_alternatives_updater_install_and_set(self):
        self.gdm_installer.install()

        self.gresource.move.assert_called_once()
        self.alternatives_updater.install_and_set.assert_called_once()