import os
import shutil
import subprocess
import unittest
from unittest.mock import patch, MagicMock

import pytest

from scripts import config
from scripts.utils.gresource import MissingDependencyError
from scripts.utils.gresource.gresource_compiler import GresourceCompiler
from ..._helpers.dummy_logger_factory import DummyLoggerFactory
from ..._helpers.dummy_runner import DummyRunner


class GresourceCompilerTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_folder = os.path.join(config.temp_tests_folder, "gresource_compiler_temp")
        self.target_file = os.path.join(self.temp_folder, "test.gresource")

        self.logger = DummyLoggerFactory()
        self.runner = DummyRunner()

        self.compiler = GresourceCompiler(self.temp_folder, self.target_file,
                                          logger_factory=self.logger, runner=self.runner)


    def tearDown(self):
        shutil.rmtree(self.temp_folder, ignore_errors=True)

    def test_compile_calls_correct_methods(self):
        """Test that compile calls the right methods in sequence."""
        with (
            patch.object(self.compiler, '_create_gresource_xml') as mock_create_xml,
            patch.object(self.compiler, '_compile_resources') as mock_compile
        ):
            self.compiler.compile()

            # Verify methods were called correctly in order
            mock_create_xml.assert_called_once()
            mock_compile.assert_called_once()

    def test_create_gresource_xml(self):
        """Test that _create_gresource_xml creates the XML file with correct content."""
        with (
            patch("builtins.open", create=True) as mock_open,
            patch.object(self.compiler, '_generate_gresource_xml') as mock_generate
        ):
            mock_generate.return_value = "<xml>test content</xml>"
            mock_file = MagicMock()
            mock_open.return_value.__enter__.return_value = mock_file

            self.compiler._create_gresource_xml()

            mock_open.assert_called_once_with(self.compiler.gresource_xml, 'w')
            mock_file.write.assert_called_once_with("<xml>test content</xml>")

    def test_generate_gresource_xml(self):
        """Test that _generate_gresource_xml creates correct XML structure."""
        with patch.object(self.compiler, '_get_files_to_include') as mock_get_files:
            mock_get_files.return_value = ["<file>file1.css</file>", "<file>subdir/file2.css</file>"]

            result = self.compiler._generate_gresource_xml()

            assert "<?xml version=" in result
            assert "<gresources>" in result
            assert "<gresource prefix=\"/org/gnome/shell/theme\">" in result
            assert "<file>file1.css</file>" in result
            assert "<file>subdir/file2.css</file>" in result

    def test_get_files_to_include(self):
        """Test that _get_files_to_include finds and formats files correctly."""
        self.__create_dummy_files_in_temp()

        result = self.compiler._get_files_to_include()

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

    def test_compile_resources(self):
        """Test that _compile_resources runs the correct subprocess command."""
        with patch.object(self.runner, "run") as mock_run:
            self.compiler._compile_resources()

            mock_run.assert_called_once()
            args = mock_run.call_args[0][0]
            assert args[0] == "glib-compile-resources"
            assert args[2] == self.temp_folder
            assert args[4] == self.compiler.target_file
            assert args[5] == self.compiler.gresource_xml

    def test_compile_resources_file_not_found(self):
        """Test that _compile_resources raises appropriate error when command not found."""
        with (
            patch.object(self.runner, "run", side_effect=FileNotFoundError("glib-compile-resources not found")),
            patch("builtins.print")
        ):
            with pytest.raises(MissingDependencyError):
                self.compiler._compile_resources()

    def test_try_compile_resources_called_process_error(self):
        """Test handling of subprocess execution failures."""
        process_error = subprocess.CalledProcessError(1, "glib-compile-resources", output="Failed to compile")
        with patch.object(self.runner, "run", side_effect=process_error):
            with pytest.raises(subprocess.CalledProcessError):
                self.compiler._try_compile_resources()

    def test_compile_resources_other_file_not_found_error(self):
        """Test that other FileNotFoundError exceptions are propagated."""
        with patch.object(self.runner, "run", side_effect=FileNotFoundError("Some other file not found")):
            with pytest.raises(FileNotFoundError):
                self.compiler._compile_resources()