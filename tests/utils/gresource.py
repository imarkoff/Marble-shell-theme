import os
import shutil
import unittest

import pytest
from unittest.mock import patch, MagicMock
from scripts import config

from scripts.utils.gresource import Gresource, GresourceBackupNotFoundError, MissingDependencyError


class DummyConsoleLine:
    def update(self, msg):
        pass
    def success(self, msg):
        pass


@patch("scripts.utils.console.Console.Line", return_value=DummyConsoleLine())
class GresourceTestCase(unittest.TestCase):
    def setUp(self):
        self.gresource_file = "test.gresource"
        self.temp_folder = os.path.join(config.temp_tests_folder, "gresource_temp")
        self.destination = os.path.join(config.temp_tests_folder, "gresource_dest")
        self.gresource_instance = Gresource(self.gresource_file, self.temp_folder, self.destination)

    def tearDown(self):
        self.__try_rmtree(self.temp_folder)
        self.__try_rmtree(self.destination)

    def getActiveSourceGresource(self):
        return self.gresource_instance._active_source_gresource

    def getBackupGresource(self):
        return self.gresource_instance._backup_gresource

    @staticmethod
    def __try_rmtree(path):
        try:
            shutil.rmtree(path)
        except FileNotFoundError:
            pass

    def test_use_backup_gresource(self, mock_console):
        backup_gresource = self.__create_dummy_file(self.getBackupGresource())

        self.gresource_instance.use_backup_gresource()

        assert self.getActiveSourceGresource() == backup_gresource

        self.__try_remove_file(backup_gresource)

    @staticmethod
    def __create_dummy_file(file_path: str):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write("dummy content")
        return file_path

    @staticmethod
    def __try_remove_file(file_path: str):
        try:
            os.remove(file_path)
        except FileNotFoundError:
            pass

    def test_use_backup_gresource_not_found(self, mock_console):
        self.__try_remove_file(self.getBackupGresource())

        with pytest.raises(GresourceBackupNotFoundError):
            self.gresource_instance.use_backup_gresource()

    def test_extract_calls_correct_methods(self, mock_console):
        with (
            patch.object(self.gresource_instance, '_get_resources_list') as mock_get_list,
            patch.object(self.gresource_instance, '_extract_resources') as mock_extract
        ):
            resources = ["resource1", "resource2"]
            mock_get_list.return_value = resources

            self.gresource_instance.extract()

            mock_get_list.assert_called_once()
            mock_extract.assert_called_once_with(resources)

    def test_get_resources_list(self, mock_console):
        """Test that resources are correctly listed from the gresource file."""
        test_resources = ["/org/gnome/shell/theme/file1.css", "/org/gnome/shell/theme/file2.css"]

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = self.__mock_gresources_list(
                stdout="\n".join(test_resources),
                stderr=""
            )

            result = self.gresource_instance._get_resources_list()

            assert result == test_resources
            mock_run.assert_called_once()
            assert mock_run.call_args[0][0][1] == "list"

    @staticmethod
    def __mock_gresources_list(stdout: str, stderr: str):
        mock_result = MagicMock()
        mock_result.stdout = stdout
        mock_result.stderr = stderr
        return mock_result

    def test_get_resources_list_error(self, mock_console):
        """Test that an exception is raised when gresource fails to list resources."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = self.__mock_gresources_list(
                stdout="",
                stderr="Error: gresource failed"
            )

            with pytest.raises(Exception):
                self.gresource_instance._get_resources_list()

    def test_extract_resources(self, mock_console):
        """Test that resources are correctly extracted."""
        test_resources = [
            "/org/gnome/shell/theme/file1.css",
            "/org/gnome/shell/theme/subdir/file2.css"
        ]

        with (
            patch("subprocess.run") as mock_run,
            patch("os.makedirs") as mock_makedirs,
            patch("builtins.open", create=True)
        ):
            self.gresource_instance._extract_resources(test_resources)

            assert mock_makedirs.call_count == 2
            assert mock_run.call_count == 2
            for i, resource in enumerate(test_resources):
                args_list = mock_run.call_args_list[i][0][0]
                assert args_list[1] == "extract"
                assert args_list[3] == resource

    def test_extract_resources_file_not_found(self, mock_console):
        """Test that an Exception is raised when gresource is not found."""
        test_resources = ["/org/gnome/shell/theme/file1.css"]

        with (
            patch("subprocess.run", side_effect=FileNotFoundError("gresource not found")),
            patch("builtins.print")
        ):
            with pytest.raises(MissingDependencyError):
                self.gresource_instance._extract_resources(test_resources)

    def test_compile_calls_correct_methods(self, mock_console):
        """Test that compile calls the right methods in sequence."""
        with patch.object(self.gresource_instance, '_create_gresource_xml') as mock_create_xml, \
                patch.object(self.gresource_instance, '_compile_resources') as mock_compile:
            # Call the method
            self.gresource_instance.compile()

            # Verify methods were called correctly in order
            mock_create_xml.assert_called_once()
            mock_compile.assert_called_once()

    def test_create_gresource_xml(self, mock_console):
        """Test that _create_gresource_xml creates the XML file with correct content."""
        with patch("builtins.open", create=True) as mock_open, \
                patch.object(self.gresource_instance, '_generate_gresource_xml') as mock_generate:
            mock_generate.return_value = "<xml>test content</xml>"
            mock_file = MagicMock()
            mock_open.return_value.__enter__.return_value = mock_file

            # Call the method
            self.gresource_instance._create_gresource_xml()

            # Verify file was written with correct content
            mock_open.assert_called_once_with(self.gresource_instance._gresource_xml, 'w')
            mock_file.write.assert_called_once_with("<xml>test content</xml>")

    def test_generate_gresource_xml(self, mock_console):
        """Test that _generate_gresource_xml creates correct XML structure."""
        with patch.object(self.gresource_instance, '_get_files_to_include') as mock_get_files:
            mock_get_files.return_value = ["<file>file1.css</file>", "<file>subdir/file2.css</file>"]

            result = self.gresource_instance._generate_gresource_xml()

            # Check XML structure
            assert "<?xml version=" in result
            assert "<gresources>" in result
            assert "<gresource prefix=\"/org/gnome/shell/theme\">" in result
            assert "<file>file1.css</file>" in result
            assert "<file>subdir/file2.css</file>" in result

    def test_get_files_to_include(self, mock_console):
        """Test that _get_files_to_include finds and formats files correctly."""
        self.__create_dummy_files_in_temp()

        result = self.gresource_instance._get_files_to_include()

        assert len(result) == 2
        assert "<file>file1.css</file>" in result
        assert "<file>subdir/file2.css</file>" in result

    def __create_dummy_files_in_temp(self):
        os.makedirs(self.temp_folder, exist_ok=True)
        test_file1 = os.path.join(self.temp_folder, "file1.css")
        test_subdir = os.path.join(self.temp_folder, "subdir")
        os.makedirs(test_subdir, exist_ok=True)
        test_file2 = os.path.join(test_subdir, "file2.css")

        with open(test_file1, 'w') as f:
            f.write("test content")
        with open(test_file2, 'w') as f:
            f.write("test content")

    def test_compile_resources(self, mock_console):
        """Test that _compile_resources runs the correct subprocess command."""
        with patch("subprocess.run") as mock_run:
            self.gresource_instance._compile_resources()

            mock_run.assert_called_once()
            args = mock_run.call_args[0][0]
            assert args[0] == "glib-compile-resources"
            assert args[2] == self.temp_folder
            assert args[4] == self.gresource_instance._temp_gresource
            assert args[5] == self.gresource_instance._gresource_xml

    def test_compile_resources_file_not_found(self, mock_console):
        """Test that _compile_resources raises appropriate error when command not found."""
        with patch("subprocess.run", side_effect=FileNotFoundError("glib-compile-resources not found")), \
                patch("builtins.print"):
            with pytest.raises(MissingDependencyError):
                self.gresource_instance._compile_resources()

    def test_backup_gresource(self, mock_console):
        """Test that backup_gresource creates a backup of the gresource file."""
        self.__create_dummy_file(self.gresource_instance._destination_gresource)

        self.gresource_instance.backup()

        assert os.path.exists(self.gresource_instance._backup_gresource)

    def test_restore_gresource(self, mock_console):
        """Test that restore_gresource restores the gresource file from backup."""
        self.__create_dummy_file(self.gresource_instance._backup_gresource)

        self.gresource_instance.restore()

        assert os.path.exists(self.gresource_instance._destination_gresource)
        assert not os.path.exists(self.gresource_instance._backup_gresource)

    def test_restore_gresource_backup_not_found(self, mock_console):
        """Test that restore_gresource raises an error if backup not found."""
        self.__try_remove_file(self.gresource_instance._backup_gresource)

        with pytest.raises(GresourceBackupNotFoundError):
            self.gresource_instance.restore()

    def test_move_with_correct_permissions(self, mock_console):
        """Test that move changes permissions correctly."""
        self.__create_dummy_file(self.gresource_instance._temp_gresource)
        self.__create_dummy_file(self.gresource_instance._destination_gresource)

        with patch("subprocess.run") as mock_run:
            self.gresource_instance.move()

            assert os.path.exists(self.gresource_instance._destination_gresource)
            permissions = oct(os.stat(self.gresource_instance._destination_gresource).st_mode)[-3:]
            assert permissions == "644"


if __name__ == "__main__":
    unittest.main()