import os
import shutil
import unittest
from unittest.mock import patch, MagicMock

import pytest

from scripts import config
from scripts.utils.gresource import MissingDependencyError
from scripts.utils.gresource.gresource_extractor import GresourceExtractor
from ..._helpers.dummy_logger_factory import DummyLoggerFactory
from ..._helpers.dummy_runner import DummyRunner


class GresourceExtractorTestCase(unittest.TestCase):
    def setUp(self):
        self.gresource_file = "test.gresource"
        self.temp_folder = os.path.join(config.temp_tests_folder, "gresource_extractor_temp")
        self.destination = os.path.join(config.temp_tests_folder, "gresource_extractor_dest")

        self.logger = DummyLoggerFactory()
        self.runner = DummyRunner()

        self.extractor = GresourceExtractor(
            self.gresource_file, self.temp_folder, 
            logger_factory=self.logger, runner=self.runner
        )

    def tearDown(self):
        shutil.rmtree(self.temp_folder, ignore_errors=True)
        shutil.rmtree(self.destination, ignore_errors=True)
        
    def test_extract_calls_correct_methods(self):
        with (
            patch.object(self.extractor, '_get_resources_list') as mock_get_list,
            patch.object(self.extractor, '_extract_resources') as mock_extract
        ):
            resources = ["resource1", "resource2"]
            mock_get_list.return_value = resources

            self.extractor.extract()

            mock_get_list.assert_called_once()
            mock_extract.assert_called_once_with(resources)

    def test_get_resources_list(self):
        """Test that resources are correctly listed from the gresource file."""
        test_resources = ["/org/gnome/shell/theme/file1.css", "/org/gnome/shell/theme/file2.css"]

        with patch.object(self.runner, "run") as mock_run:
            mock_run.return_value = self.__mock_gresources_list(
                stdout="\n".join(test_resources),
                stderr=""
            )

            result = self.extractor._get_resources_list()

            assert result == test_resources
            mock_run.assert_called_once()
            assert mock_run.call_args[0][0][1] == "list"

    @staticmethod
    def __mock_gresources_list(stdout: str, stderr: str):
        mock_result = MagicMock()
        mock_result.stdout = stdout
        mock_result.stderr = stderr
        return mock_result

    def test_get_resources_list_error(self):
        """Test that an exception is raised when gresource fails to list resources."""
        with patch.object(self.runner, "run",
                          side_effect=Exception("Error: gresource failed")):

            with pytest.raises(Exception):
                self.extractor._get_resources_list()

    def test_extract_resources(self):
        """Test that resources are correctly extracted."""
        test_resources = [
            "/org/gnome/shell/theme/file1.css",
            "/org/gnome/shell/theme/subdir/file2.css"
        ]

        with (
            patch.object(self.runner, "run") as mock_run,
            patch("os.makedirs") as mock_makedirs,
            patch("builtins.open", create=True)
        ):
            self.extractor._extract_resources(test_resources)

            assert mock_makedirs.call_count == 2
            assert mock_run.call_count == 2
            for i, resource in enumerate(test_resources):
                args_list = mock_run.call_args_list[i][0][0]
                assert args_list[1] == "extract"
                assert args_list[3] == resource

    def test_extract_resources_file_not_found(self):
        with (
            patch.object(self.runner, "run",
                         side_effect=FileNotFoundError("gresource not found")),
            patch("builtins.print")
        ):
            with pytest.raises(MissingDependencyError):
                self.extractor.extract()

    def test_try_extract_resources(self):
        resources = ["/org/gnome/shell/theme/file.css"]

        with (
            patch("os.makedirs"),
            patch("builtins.open", create=True) as mock_open
        ):
            mock_file = MagicMock()
            mock_open.return_value.__enter__.return_value = mock_file

            self.extractor._extract_resources(resources)

            expected_path = os.path.join(self.temp_folder, "file.css")
            mock_open.assert_called_once_with(expected_path, 'wb')

    def test_empty_resource_list(self):
        self.extractor._extract_resources([])