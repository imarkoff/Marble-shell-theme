from unittest import TestCase
from unittest.mock import Mock

from scripts.utils.global_theme.gdm import GDMTheme
from scripts.utils.global_theme.gdm_installer import GDMThemeInstaller
from scripts.utils.global_theme.gdm_preparer import GDMThemePreparer
from scripts.utils.global_theme.gdm_remover import GDMThemeRemover


class GDMTestCase(TestCase):
    def setUp(self):
        self.preparer = Mock(spec=GDMThemePreparer)
        self.installer = Mock(spec=GDMThemeInstaller)
        self.remover = Mock(spec=GDMThemeRemover)

        self.gdm = GDMTheme(self.preparer, self.installer, self.remover)

    def test_prepare_uses_backup_if_installed(self):
        self.installer.is_installed.return_value = True

        self.gdm.prepare()

        self.preparer.use_backup_as_source.assert_called_once()

    def test_prepare_does_not_use_backup_if_not_installed(self):
        self.installer.is_installed.return_value = False

        self.gdm.prepare()

        self.preparer.use_backup_as_source.assert_not_called()

    def test_prepare_calls_preparer_prepare_and_sets_themes(self):
        mock_theme = Mock()
        self.preparer.prepare.return_value = [mock_theme]

        self.gdm.prepare()

        self.preparer.prepare.assert_called_once()
        self.assertEqual(self.gdm.themes, [mock_theme])

    def test_install_correctly_passes_arguments_to_installer_compile(self):
        hue = 100
        name = "test_theme"
        sat = 0.5

        self.gdm.install(hue, name, sat)

        self.installer.compile.assert_called_once_with(self.gdm.themes, hue, name, sat)

    def test_install_calls_installer_backup_if_not_installed(self):
        self.installer.is_installed.return_value = False

        self.gdm.install(100, "test_theme")

        self.installer.backup.assert_called_once()

    def test_install_does_not_call_installer_backup_if_installed(self):
        self.installer.is_installed.return_value = True

        self.gdm.install(100, "test_theme")

        self.installer.backup.assert_not_called()

    def test_install_calls_installer_install(self):
        self.gdm.install(100, "test_theme")

        self.installer.install.assert_called_once()

    def test_remove_calls_installer_remove_if_installed(self):
        self.installer.is_installed.return_value = True

        self.gdm.remove()

        self.remover.remove.assert_called_once()

    def test_remove_calls_installer_warn_if_not_installed(self):
        self.installer.is_installed.return_value = False

        self.gdm.remove()

        self.remover.remove.assert_not_called()