from unittest import TestCase
from unittest.mock import MagicMock

from scripts.utils.alternatives_updater import AlternativesUpdater
from scripts.utils.global_theme.ubuntu_alternatives_updater import UbuntuGDMAlternativesUpdater


class UbuntuGDMUpdateAlternativesTestCase(TestCase):
    def setUp(self):
        self.updater = MagicMock(spec=AlternativesUpdater)
        self.ubuntu_updater = UbuntuGDMAlternativesUpdater(
            alternatives_updater=self.updater
        )

    def test_custom_destination_updates_correctly(self):
        custom_destination_dir = "/custom/path"
        custom_destination_file = "custom_file.gresource"

        self.ubuntu_updater.with_custom_destination(
            custom_destination_dir, custom_destination_file
        )

        self.assertEqual(
            self.ubuntu_updater.destination_dir, custom_destination_dir
        )
        self.assertEqual(
            self.ubuntu_updater.destination_file, custom_destination_file
        )

    def test_install_and_set_calls_updater_correctly(self):
        priority = 100
        self.ubuntu_updater.install_and_set(priority)

        self.updater.install_and_set.assert_called_once_with(
            link=self.ubuntu_updater.ubuntu_gresource_path,
            name=self.ubuntu_updater.ubuntu_gresource_link_name,
            path=self.ubuntu_updater.gnome_gresource_path,
            priority=priority
        )

    def test_remove_calls_updater_correctly(self):
        self.ubuntu_updater.remove()

        self.updater.remove.assert_called_once_with(
            name=self.ubuntu_updater.ubuntu_gresource_link_name,
            path=self.ubuntu_updater.gnome_gresource_path
        )