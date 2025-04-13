from unittest import TestCase
from unittest.mock import Mock

from scripts.types.installation_color import InstallationMode
from scripts.utils.global_theme.gdm_builder import GDMThemeBuilder


class GDMBuilderTestCase(TestCase):
    def setUp(self):
        self.colors_provider = Mock()
        self.builder = GDMThemeBuilder(colors_provider=self.colors_provider)

    def test_with_mode_sets_correct_mode(self):
        self.builder._mode = None
        mode: InstallationMode = "dark"

        builder = self.builder.with_mode(mode)

        self.assertEqual(builder._mode, mode)

    def test_with_filled_sets_correct_filled_state(self):
        self.builder._is_filled = False
        is_filled = True

        builder = self.builder.with_filled(is_filled)

        self.assertEqual(builder._is_filled, is_filled)

    def test_with_logger_factory_sets_specified_logger_factory(self):
        logger_factory = Mock()
        builder = self.builder.with_logger_factory(logger_factory)
        self.assertEqual(builder._logger_factory, logger_factory)

    def test_with_gresource_sets_specified_gresource(self):
        gresource = Mock()
        builder = self.builder.with_gresource(gresource)
        self.assertEqual(builder._gresource, gresource)

    def test_with_ubuntu_gdm_alternatives_updater_sets_specified_updater(self):
        alternatives_updater = Mock()
        builder = self.builder.with_ubuntu_gdm_alternatives_updater(alternatives_updater)
        self.assertEqual(builder._ubuntu_gdm_alternatives_updater, alternatives_updater)

    def test_with_preparer_sets_specified_preparer(self):
        preparer = Mock()
        builder = self.builder.with_preparer(preparer)
        self.assertEqual(builder._preparer, preparer)

    def test_with_installer_sets_specified_installer(self):
        installer = Mock()
        builder = self.builder.with_installer(installer)
        self.assertEqual(builder._installer, installer)

    def test_with_remover_sets_specified_remover(self):
        remover = Mock()
        builder = self.builder.with_remover(remover)
        self.assertEqual(builder._remover, remover)

    def test_resolve_logger_factory_initializes_logger_factory(self):
        self.builder._logger_factory = None

        self.builder._resolve_logger_factory()

        self.assertIsNotNone(self.builder._logger_factory)

    def test_resolve_gresource_initializes_gresource(self):
        self.builder._logger_factory = Mock()
        self.builder._gresource = None

        self.builder._resolve_gresource()

        self.assertIsNotNone(self.builder._gresource)

    def test_builder_supports_chaining(self):
        theme = self.builder.with_mode("dark").with_filled(True).build()

        self.assertIsNotNone(theme)

    def test_resolve_ubuntu_gdm_alternatives_updater_initializes_gresource(self):
        self.builder._logger_factory = Mock()
        self.builder._gresource = Mock()
        self.builder._ubuntu_gdm_alternatives_updater = None
        self.builder._resolve_ubuntu_gdm_alternatives_updater()
        self.assertIsNotNone(self.builder._ubuntu_gdm_alternatives_updater)

    def test_resolve_preparer_initializes_preparer(self):
        self.builder._logger_factory = Mock()
        self.builder._gresource = Mock()
        self.builder._ubuntu_gdm_alternatives_updater = Mock()
        self.builder._preparer = None

        self.builder._resolve_preparer()

        self.assertIsNotNone(self.builder._preparer)

    def test_resolve_installer_initializes_installer(self):
        self.builder._gresource = Mock()
        self.builder._ubuntu_gdm_alternatives_updater = Mock()
        self.builder._installer = None

        self.builder._resolve_installer()

        self.assertIsNotNone(self.builder._installer)

    def test_resolve_remover_initializes_remover(self):
        self.builder._gresource = Mock()
        self.builder._ubuntu_gdm_alternatives_updater = Mock()
        self.builder._remover = None

        self.builder._resolve_remover()

        self.assertIsNotNone(self.builder._remover)

    def test_build_resolves_dependencies(self):
        self.builder._resolve_logger_factory = Mock()
        self.builder._resolve_gresource = Mock()
        self.builder._resolve_ubuntu_gdm_alternatives_updater = Mock()
        self.builder._resolve_preparer = Mock()
        self.builder._resolve_installer = Mock()
        self.builder._resolve_remover = Mock()

        self.builder.build()

        self.builder._resolve_logger_factory.assert_called_once()
        self.builder._resolve_gresource.assert_called_once()
        self.builder._resolve_ubuntu_gdm_alternatives_updater.assert_called_once()
        self.builder._resolve_preparer.assert_called_once()
        self.builder._resolve_installer.assert_called_once()
        self.builder._resolve_remover.assert_called_once()

    def test_build_correctly_builds_gdm_theme(self):
        self.builder._preparer = Mock()
        self.builder._installer = Mock()
        self.builder._remover = Mock()

        result = self.builder.build()

        self.assertEqual(result.preparer, self.builder._preparer)
        self.assertEqual(result.installer, self.builder._installer)
        self.assertEqual(result.remover, self.builder._remover)

    def test_build_with_explicit_dependencies_works_correctly(self):
        preparer = Mock()
        installer = Mock()
        remover = Mock()
        builder = (self.builder
                   .with_preparer(preparer)
                   .with_installer(installer)
                   .with_remover(remover))

        result = builder.build()

        self.assertEqual(result.preparer, preparer)
        self.assertEqual(result.installer, installer)
        self.assertEqual(result.remover, remover)