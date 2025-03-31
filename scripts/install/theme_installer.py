import argparse

from scripts.install.colors_definer import ColorsDefiner
from scripts.theme import Theme
from scripts.tweaks_manager import TweaksManager


class ThemeInstaller:
    theme: Theme

    def __init__(self, args: argparse.Namespace, colors: ColorsDefiner):
        self.args = args
        self.colors = colors
        self.stop_after_first_installed_color = False
        self._define_theme()

    def remove(self):
        pass

    def install(self):
        self.theme.prepare()
        self._apply_tweaks_to_theme()
        self._apply_colors()

    def _define_theme(self):
        pass

    def _install_theme(self, hue, theme_name, sat):
        pass

    def _apply_tweaks_to_theme(self):
        pass

    def _apply_tweaks(self, theme):
        tweaks_manager = TweaksManager()
        tweaks_manager.apply_tweaks(self.args, theme, self.colors)

    def _apply_colors(self):
        installed_any = False

        if self.args.hue:
            installed_any = True
            self._apply_custom_color()
        else:
            installed_any = self._apply_default_color()

        if not installed_any:
            raise Exception('No color arguments specified. Use -h or --help to see the available options.')

    def _apply_custom_color(self):
        name = self.args.name
        hue = self.args.hue
        sat = self.args.sat

        theme_name = name if name else f'hue{hue}'
        self._install_theme(hue, theme_name, sat)

    def _apply_default_color(self) -> bool:
        colors = self.colors.colors
        args = self.args
        installed_any = False

        for color, values in colors.items():
            if self.args.all or getattr(self.args, color, False):
                hue = values.get('h')
                sat = values.get('s', args.sat)  # if saturation already defined in color (gray)

                self._install_theme(hue, color, sat)
                installed_any = True

                if self.stop_after_first_installed_color:
                    break

        return installed_any