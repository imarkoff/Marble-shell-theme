import os

from scripts import config
from scripts.gdm import GlobalTheme
from scripts.install.theme_installer import ThemeInstaller


class GlobalThemeInstaller(ThemeInstaller):
    theme: GlobalTheme

    def remove(self):
        gdm_rm_status = self.theme.remove()
        if gdm_rm_status == 0:
            print("GDM theme removed successfully.")

    def _define_theme(self):
        gdm_temp = os.path.join(config.temp_folder, config.gdm_folder)
        self.theme = GlobalTheme(self.colors, f"{config.raw_theme_folder}/{config.gnome_folder}",
                                config.global_gnome_shell_theme, config.gnome_shell_gresource,
                                gdm_temp, mode=self.args.mode, is_filled=self.args.filled)

    def _install_theme(self, hue, theme_name, sat):
        self.theme.prepare()
        self.theme.install(hue, sat)

    def _apply_tweaks_to_theme(self):
        for theme in self.theme.themes:
            self._apply_tweaks(theme.theme)