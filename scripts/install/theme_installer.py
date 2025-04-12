import argparse
import concurrent.futures
from abc import ABC, abstractmethod

from scripts.install.colors_definer import ColorsDefiner
from scripts.types.theme_base import ThemeBase
from scripts.tweaks_manager import TweaksManager


class ThemeInstaller(ABC):
    """Base class for theme installers"""
    theme: ThemeBase

    def __init__(self, args: argparse.Namespace, colors: ColorsDefiner):
        self.args = args
        self.colors = colors
        self._define_theme()

    @abstractmethod
    def remove(self):
        """Method for removing already installed themes"""
        pass

    def install(self):
        self.theme.prepare()
        self._apply_tweaks_to_theme()
        self._apply_colors()
        self._after_install()

    @abstractmethod
    def _define_theme(self):
        """Here is the place to define the theme object"""
        pass

    @abstractmethod
    def _apply_tweaks_to_theme(self):
        """Should apply the tweaks for prepared theme"""
        pass

    @abstractmethod
    def _after_install(self):
        """Method to be called after the theme is installed. Can be used for logging or other actions"""
        pass

    def _apply_tweaks(self, theme):
        """This method should be called in the _apply_tweaks_to_theme method"""
        tweaks_manager = TweaksManager()
        tweaks_manager.apply_tweaks(self.args, theme, self.colors)

    def _apply_colors(self):
        if self.args.hue:
            self._apply_custom_color()
            return

        if self._apply_default_color():
            return

        raise Exception('No color arguments specified. Use -h or --help to see the available options.')

    def _apply_custom_color(self):
        name = self.args.name
        hue = self.args.hue
        sat = self.args.sat

        theme_name = name if name else f'hue{hue}'
        self.theme.install(hue, theme_name, sat)

    def _apply_default_color(self) -> bool:
        colors = self.colors.colors
        args = self.args

        colors_to_install = []
        for color, values in colors.items():
            if args.all or getattr(args, color, False):
                hue = values.get('h')
                sat = values.get('s', args.sat)
                colors_to_install.append((hue, color, sat))

        if not colors_to_install:
            return False
        self._run_concurrent_installation(colors_to_install)
        return True

    def _run_concurrent_installation(self, colors_to_install):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.theme.install, hue, color, sat)
                       for hue, color, sat in colors_to_install]

            for future in concurrent.futures.as_completed(futures):
                future.result()