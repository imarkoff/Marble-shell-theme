import os.path

from scripts import config
from scripts.utils.alternatives_updater import AlternativesUpdater


class UbuntuGDMAlternativesUpdater:
    """
    Manages update-alternatives for Ubuntu GDM themes.

    This class handles:
    - Creating alternatives for GDM theme files
    - Setting installed theme as the active alternative
    - Removing theme alternatives during uninstallation
    """
    def __init__(self, alternatives_updater: AlternativesUpdater):
        """
        :param alternatives_updater: Handler for update-alternatives operations
        """
        self.ubuntu_gresource_link_name = config.ubuntu_gresource_link
        self.destination_dir = config.global_gnome_shell_theme
        self.destination_file = config.gnome_shell_gresource

        self.alternatives_updater = alternatives_updater

        self._update_gresource_paths()

    def _update_gresource_paths(self):
        self.ubuntu_gresource_path = os.path.join(self.destination_dir, self.ubuntu_gresource_link_name)
        self.gnome_gresource_path = os.path.join(self.destination_dir, self.destination_file)

    def with_custom_destination(self, destination_dir: str, destination_file: str):
        """Set custom destination directory and file for the theme."""
        self.destination_dir = destination_dir
        self.destination_file = destination_file
        self._update_gresource_paths()
        return self

    def install_and_set(self, priority: int = 0):
        """
        Add theme as an alternative and set it as active.

        This creates a system alternative for the GDM theme and
        makes it the active selection with the specified priority.

        :param priority: Priority level for the alternative (higher wins in conflicts)
        """
        self.alternatives_updater.install_and_set(
            link=self.ubuntu_gresource_path,
            name=self.ubuntu_gresource_link_name,
            path=self.gnome_gresource_path,
            priority=priority
        )

    def remove(self):
        """
        Remove the theme alternative from the system.

        This removes the previously installed alternative, allowing
        the system to fall back to the default GDM theme.
        """
        self.alternatives_updater.remove(
            name=self.ubuntu_gresource_link_name,
            path=self.gnome_gresource_path
        )
