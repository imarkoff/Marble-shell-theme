import os.path
import shutil
import unittest

from scripts import config
from scripts.utils.theme.theme_temp_manager import ThemeTempManager
from ..._helpers import create_dummy_file


class ThemeTempManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.source_folder = os.path.join(config.temp_tests_folder, "theme_temp_manager_source")
        self.temp_folder = os.path.join(config.temp_tests_folder, "theme_temp_manager")
        self.manager = ThemeTempManager(temp_folder=self.temp_folder)

    def tearDown(self):
        shutil.rmtree(self.temp_folder, ignore_errors=True)
        shutil.rmtree(self.source_folder, ignore_errors=True)

    @staticmethod
    def _verify_file_copied(source, destination):
        assert os.path.exists(destination)
        assert os.path.getsize(destination) == os.path.getsize(source)
        assert open(destination).read() == open(source).read()

    def test_file_copies_correctly_to_temp(self):
        test_file_name = "test_file.txt"
        test_file_location = os.path.join(self.source_folder, test_file_name)
        create_dummy_file(test_file_location)

        self.manager.copy_to_temp(test_file_location)

        final_file_location = os.path.join(self.temp_folder, test_file_name)
        self._verify_file_copied(test_file_location, final_file_location)
        os.remove(final_file_location)

    def test_directory_content_copies_correctly_to_temp(self):
        test_dir_name = "test_dir"
        test_dir_location = os.path.join(self.source_folder, test_dir_name)
        os.makedirs(test_dir_location, exist_ok=True)

        test_file_name = "test_file.txt"
        test_file_location = os.path.join(test_dir_location, test_file_name)
        create_dummy_file(test_file_location)

        self.manager.copy_to_temp(test_dir_location)

        final_file_location = os.path.join(self.temp_folder, test_file_name)
        self._verify_file_copied(test_file_location, final_file_location)
        os.remove(final_file_location)

    def test_cleanup_removes_temp_folders(self):
        css_folder = os.path.join(self.temp_folder, ".css")
        versions_folder = os.path.join(self.temp_folder, ".versions")
        os.makedirs(css_folder, exist_ok=True)
        os.makedirs(versions_folder, exist_ok=True)

        self.manager.cleanup()

        assert not os.path.exists(css_folder)
        assert not os.path.exists(versions_folder)

    def test_cleanup_non_existent_folders_do_not_raise_error(self):
        css_folder = os.path.join(self.temp_folder, ".css")
        versions_folder = os.path.join(self.temp_folder, ".versions")

        self.manager.cleanup()

        # Check that no error is raised and the method completes successfully
        assert not os.path.exists(css_folder)
        assert not os.path.exists(versions_folder)