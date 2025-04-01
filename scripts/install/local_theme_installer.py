import os.path

from scripts import config
from scripts.install.theme_installer import ThemeInstaller
from scripts.theme import Theme
from scripts.utils import remove_files


class LocalThemeInstaller(ThemeInstaller):
    theme: Theme

    def remove(self):
        colors = self.colors.colors
        remove_files(self.args, colors)

    def _define_theme(self):
        theme_folder = os.path.join(config.raw_theme_folder, config.gnome_folder)
        self.theme = Theme("gnome-shell", self.colors, theme_folder,
                              config.themes_folder, config.temp_folder,
                              mode=self.args.mode, is_filled=self.args.filled)

    def _install_theme(self, hue, theme_name, sat):
        self.theme.prepare()
        self.theme.install(hue, theme_name, sat)

    def _apply_tweaks_to_theme(self):
        self._apply_tweaks(self.theme)

    def _after_install(self):
        print("\nTheme installed successfully.")