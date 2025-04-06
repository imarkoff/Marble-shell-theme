class GresourceBackupNotFoundError(FileNotFoundError):
    def __init__(self, location: str = None):
        if location:
            super().__init__(f"Gresource backup file not found: {location}")
        else:
            super().__init__("Gresource backup file not found.")


class MissingDependencyError(Exception):
    def __init__(self, dependency: str):
        super().__init__(f"Missing required dependency: {dependency}")
        self.dependency = dependency


def raise_gresource_error(tool: str, e: Exception):
    print(f"Error: '{tool}' command not found.")
    print("Please install the glib2-devel package:")
    print(" - For Fedora/RHEL: sudo dnf install glib2-devel")
    print(" - For Ubuntu/Debian: sudo apt install libglib2.0-dev")
    print(" - For Arch: sudo pacman -S glib2-devel")
    raise MissingDependencyError("glib2-devel") from e
