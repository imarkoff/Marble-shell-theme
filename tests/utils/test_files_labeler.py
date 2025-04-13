import os.path
import shutil
from unittest import TestCase

from scripts import config
from scripts.utils.files_labeler import FilesLabelerFactoryImpl
from .._helpers import create_dummy_file


class FilesLabelerTestCase(TestCase):
    def setUp(self):
        self.temp_folder = os.path.join(config.temp_tests_folder, "labeler")

        self.files = ["file1.svg", "file2.png", "file3.svg"]
        self.styles_file = os.path.join(self.temp_folder, "styles-test.css")  # styles files are already labeled
        self.original_styles_content = f"body {{ background: url('./{self.files[0]}'); }}"

        self.factory = FilesLabelerFactoryImpl()

    def _generate_test_files(self):
        self.tearDown()

        for filename in self.files:
            create_dummy_file(os.path.join(self.temp_folder, filename))

        create_dummy_file(self.styles_file, self.original_styles_content)

    def tearDown(self):
        shutil.rmtree(self.temp_folder, ignore_errors=True)

    def test_append_label_correctly_labels_files(self):
        self._generate_test_files()
        label = "test"
        labeled_files = [(f, f.replace(".", f"-{label}.")) for f in self.files]
        labeler = self.factory.create(self.temp_folder)

        labeler.append_label(label)

        for original, labeled in labeled_files:
            labeled_path = os.path.join(self.temp_folder, labeled)
            original_path = os.path.join(self.temp_folder, original)
            self.assertTrue(os.path.exists(labeled_path))
            self.assertFalse(os.path.exists(original_path))

    def test_append_label_correctly_updates_references(self):
        self._generate_test_files()
        label = "test"
        replaced_file = self.files[0].replace('.', f'-{label}.')
        expected_content = f"body {{ background: url('./{replaced_file}'); }}"
        labeler = self.factory.create(self.temp_folder, self.styles_file)

        labeler.append_label(label)

        with open(self.styles_file, 'r') as file:
            actual_content = file.read()
            self.assertNotEqual(actual_content, self.original_styles_content)
            self.assertEqual(actual_content, expected_content)