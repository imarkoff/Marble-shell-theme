import functools
import subprocess
from typing import TypeAlias

from scripts.utils.logger.console import Console

PathString: TypeAlias = str | bytes

class AlternativesUpdater:
    """
    Manages update-alternatives for Ubuntu.
    Ignores errors if update-alternatives not found.
    """

    @staticmethod
    def ubuntu_specific(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except FileNotFoundError as e:
                if not "update-alternatives" in str(e):
                    raise
                return None

        return wrapper

    @staticmethod
    @ubuntu_specific
    def install_and_set(link: PathString, name: str, path: PathString, priority: int = 0):
        AlternativesUpdater.install(link, name, path, priority)
        AlternativesUpdater.set(name, path)

    @staticmethod
    @ubuntu_specific
    def install(link: str, name: str, path: PathString, priority: int = 0):
        """
        Add an alternative to the system
        :param link: Absolute path with file name where the link will be created
        :param name: Name of the alternative
        :param path: An absolute path to the file that will be linked
        :param priority: Priority of the alternative; Higher number means higher priority

        Example:
            install(/usr/share/gnome-shell/gdm-theme.gresource,
            gdm-theme.gresource, /usr/share/gnome-shell/gnome-shell-theme.gresource)
        """
        subprocess.run([
            "update-alternatives", "--install",
            link, name, str(path), str(priority)
        ], stdout=subprocess.DEVNULL, check=True)
        Console.Line().success(f"Installed {name} alternative.")

    @staticmethod
    @ubuntu_specific
    def set(name: str, path: PathString):
        """
        Set path as alternative to name in system
        :param name: Name of the alternative
        :param path: An absolute path to the file that will be linked

        Example:
            set(gdm-theme.gresource, /usr/share/gnome-shell/gnome-shell-theme.gresource)
        """
        subprocess.run([
            "update-alternatives", "--set",
            name, str(path)
        ], stdout=subprocess.DEVNULL, check=True)

    @staticmethod
    @ubuntu_specific
    def remove(name: str, path: PathString):
        """
        Remove alternative from system
        :param name: Name of the alternative
        :param path: An absolute path to the file that will be linked

        Example:
            remove(gdm-theme.gresource, /usr/share/gnome-shell/gnome-shell-theme.gresource)
        """
        subprocess.run([
            "update-alternatives", "--remove",
            name, str(path)
        ], stdout=subprocess.DEVNULL, check=True)
        Console.Line().success(f"Removed {name} alternative.")