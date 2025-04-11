import os


class SourceFolder:
    themes_folder = os.path.dirname(__file__)

    @property
    def gnome_shell(self):
        return os.path.join(self.themes_folder, "gnome-shell")