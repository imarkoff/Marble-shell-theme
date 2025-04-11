import os.path
import shutil
import unittest
from unittest.mock import patch

from scripts import config
from scripts.utils.gresource.gresource import Gresource
from ..._helpers import create_dummy_file, try_remove_file
from ..._helpers.dummy_logger_factory import DummyLoggerFactory
from ..._helpers.dummy_runner import DummyRunner


class GresourceTestCase(unittest.TestCase):
    def setUp(self):
        self.gresource_file = "test.gresource"
        self.temp_folder = os.path.join(config.temp_tests_folder, "gresource_temp")
        self.destination = os.path.join(config.temp_tests_folder, "gresource_dest")

        self.temp_file = os.path.join(self.temp_folder, self.gresource_file)
        self.destination_file = os.path.join(self.destination, self.gresource_file)

        self.logger = DummyLoggerFactory()
        self.runner = DummyRunner()

        self.gresource = Gresource(
            self.gresource_file, self.temp_folder, self.destination,
            logger_factory=self.logger, runner=self.runner
        )

    def tearDown(self):
        shutil.rmtree(self.temp_folder, ignore_errors=True)
        shutil.rmtree(self.destination, ignore_errors=True)

    def test_use_backup_gresource(self):
        destination_file = os.path.join(self.destination, self.gresource_file)
        create_dummy_file(destination_file)
        self.gresource.backup()

        self.gresource.use_backup_gresource()

        assert self.gresource._active_source_gresource != self.gresource._destination_gresource
        assert os.path.exists(self.gresource._active_source_gresource)

        try_remove_file(self.gresource._active_source_gresource)
        try_remove_file(destination_file)

    def test_use_backup_gresource_not_found(self):
        destination_file = os.path.join(self.destination, self.gresource_file)
        try_remove_file(destination_file)

        with self.assertRaises(FileNotFoundError):
            self.gresource.use_backup_gresource()

    def test_extract(self):
        """Test that extract creates and calls GresourceExtractor correctly."""
        with patch('scripts.utils.gresource.gresource.GresourceExtractor') as mock_extractor_class:
            mock_extractor_instance = mock_extractor_class.return_value

            self.gresource.extract()

            mock_extractor_class.assert_called_once_with(
                self.gresource._active_source_gresource,
                self.temp_folder,
                logger_factory=self.logger,
                runner=self.runner
            )
            mock_extractor_instance.extract.assert_called_once()

    def test_compile(self):
        """Test that compile creates and calls GresourceCompiler correctly."""
        with (patch('scripts.utils.gresource.gresource.GresourceCompiler') as mock_compiler_class):
            mock_compiler_instance = mock_compiler_class.return_value

            self.gresource.compile()

            mock_compiler_class.assert_called_once_with(
                self.temp_folder,
                self.gresource._temp_gresource,
                logger_factory=self.logger,
                runner=self.runner
            )
            mock_compiler_instance.compile.assert_called_once()

    def test_backup(self):
        create_dummy_file(self.destination_file)

        self.gresource.backup()
        backup = self.gresource.use_backup_gresource()

        assert os.path.exists(backup)
        self.gresource.restore()

    def test_backup_not_found(self):
        try_remove_file(self.destination_file)

        with self.assertRaises(FileNotFoundError):
            self.gresource.backup()

    def test_restore(self):
        destination_file = os.path.join(self.destination, self.gresource_file)
        create_dummy_file(destination_file, content="dummy content")
        self.gresource.backup()
        create_dummy_file(destination_file, content="new content")

        self.gresource.restore()

        assert os.path.exists(destination_file)
        with open(destination_file) as f:
            content = f.read()
            assert content == "dummy content"

    def test_restore_not_found(self):
        destination_file = os.path.join(self.destination, self.gresource_file)
        try_remove_file(destination_file)

        with self.assertRaises(FileNotFoundError):
            self.gresource.restore()

    def test_move(self):
        create_dummy_file(self.temp_file)

        self.gresource.move()

        assert os.path.exists(self.destination_file)

    def test_move_not_found(self):
        try_remove_file(self.temp_file)

        with self.assertRaises(FileNotFoundError):
            self.gresource.move()