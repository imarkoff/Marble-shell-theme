from unittest import TestCase
from unittest.mock import MagicMock

from scripts.utils.global_theme.gdm_remover import GDMThemeRemover
from scripts.utils.gresource import GresourceBackupNotFoundError


class GDMRemoverTestCase(TestCase):
    def setUp(self):
        self.gresource = MagicMock()
        self.alternatives_updater = MagicMock()
        self.logger = MagicMock()
        self.logger_factory = MagicMock(return_value=self.logger)

        self.remover = GDMThemeRemover(
            gresource=self.gresource,
            alternatives_updater=self.alternatives_updater,
            logger_factory=self.logger_factory
        )

        self.remover.remover_logger = MagicMock()

    def test_remove_logs_start_message(self):
        self.remover.remove()

        self.remover.remover_logger.start_removing.assert_called_once()

    def test_remove_calls_gresource_restore_and_alternatives_remove(self):
        self.remover.remove()

        self.gresource.restore.assert_called_once()
        self.alternatives_updater.remove.assert_called_once()

    def test_remove_logs_success_message(self):
        self.remover.remove()

        self.remover.remover_logger.success_removing.assert_called_once()

    def test_remove_logs_error_message_when_backup_not_found(self):
        self.gresource.restore.side_effect = GresourceBackupNotFoundError()

        self.remover.remove()

        self.remover.remover_logger.error_removing.assert_called_once()