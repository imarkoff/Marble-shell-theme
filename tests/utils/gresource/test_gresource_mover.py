import os.path
import unittest
from unittest.mock import patch

from scripts import config
from scripts.utils.gresource.gresource_mover import GresourceMover
from ..._helpers import create_dummy_file, try_remove_file
from ..._helpers.dummy_logger_factory import DummyLoggerFactory
from ..._helpers.dummy_runner import DummyRunner


class GresourceMoverTestCase(unittest.TestCase):
    def setUp(self):
        self.gresource_file = "test.gresource"
        self.source_file = os.path.join(config.temp_tests_folder, "gresource_mover_source", self.gresource_file)
        self.destination_file = os.path.join(config.temp_tests_folder, "gresource_mover_destination", self.gresource_file)

        self.logger = DummyLoggerFactory()
        self.runner = DummyRunner()

        self.mover = GresourceMover(self.source_file, self.destination_file,
                                    logger_factory=self.logger)


    def tearDown(self):
        try_remove_file(self.source_file)
        try_remove_file(self.destination_file)
        
    def test_move_with_correct_permissions(self):
        """Test that move changes permissions correctly."""
        create_dummy_file(self.source_file)

        self.mover.move()

        assert os.path.exists(self.mover.destination_file)
        permissions = oct(os.stat(self.mover.destination_file).st_mode)[-3:]
        assert permissions == "644"

    def test_move_handles_cp_error(self):
        """Test that errors during copy are properly handled."""
        with patch('shutil.copyfile', side_effect=OSError):
            with self.assertRaises(OSError):
                self.mover.move()

    def test_move_handles_chmod_error(self):
        """Test that errors during chmod are properly handled."""
        create_dummy_file(self.source_file)

        with patch('os.chmod', side_effect=PermissionError):
            with self.assertRaises(PermissionError):
                self.mover.move()