import os
import shutil
import unittest

import pytest

from scripts import config
from scripts.utils.gresource import GresourceBackupNotFoundError
from scripts.utils.gresource.gresource_backuper import GresourceBackuperManager, GresourceBackuper
from ..._helpers import create_dummy_file, try_remove_file
from ..._helpers.dummy_logger_factory import DummyLoggerFactory


class GresourceBackuperManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.gresource_file = "test.gresource"
        self.temp_folder = os.path.join(config.temp_tests_folder, "backup_temp")
        self.destination = os.path.join(config.temp_tests_folder, "backup_dest")
        self.destination_file = os.path.join(self.temp_folder, self.gresource_file)

        self.logger = DummyLoggerFactory()

        self.backuper_manager = GresourceBackuperManager(self.destination_file,
                                                         logger_factory=self.logger)

    def tearDown(self):
        shutil.rmtree(self.temp_folder, ignore_errors=True)
        shutil.rmtree(self.destination, ignore_errors=True)

    def test_get_backup(self):
        create_dummy_file(self.destination_file)

        self.backuper_manager.backup()
        backup = self.backuper_manager.get_backup()

        assert os.path.exists(backup)

    def test_backup_overwrites_existing_backup(self):
        """Test that backup properly overwrites an existing backup file."""
        create_dummy_file(self.destination_file, content="original")
        create_dummy_file(self.backuper_manager._backup_file, content="old backup")

        self.backuper_manager.backup()

        with open(self.backuper_manager._backup_file, 'r') as f:
            content = f.read()
        assert content == "original"


class GresourceBackuperTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_folder = os.path.join(config.temp_tests_folder, "backup_temp")
        self.destination_file = os.path.join(self.temp_folder, "test.gresource")
        self.backup_file = f"{self.destination_file}.backup"

        self.logger = DummyLoggerFactory()

        self.backuper = GresourceBackuper(self.destination_file, self.backup_file,
                                          logger_factory=self.logger)

        os.makedirs(self.temp_folder, exist_ok=True)

    def test_get_backup(self):
        create_dummy_file(self.backup_file)

        backup = self.backuper.get_backup()

        assert os.path.exists(backup)
        assert backup == self.backup_file

    def test_use_backup_gresource_not_found(self):
        try_remove_file(self.backup_file)

        with pytest.raises(GresourceBackupNotFoundError):
            self.backuper.get_backup()

    def test_backup_creates_backup_file(self):
        """Test direct backup functionality."""
        create_dummy_file(self.destination_file)

        self.backuper.backup()

        assert os.path.exists(self.backup_file)

    def test_backup_handles_missing_destination(self):
        """Test backup behavior when destination file doesn't exist."""
        try_remove_file(self.destination_file)

        with pytest.raises(FileNotFoundError):
            self.backuper.backup()

    def test_restore_implementation(self):
        """Test direct restore implementation."""
        create_dummy_file(self.backup_file)
        try_remove_file(self.destination_file)

        self.backuper.restore()

        assert os.path.exists(self.destination_file)
        assert not os.path.exists(self.backup_file)