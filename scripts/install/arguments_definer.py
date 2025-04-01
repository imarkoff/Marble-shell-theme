import argparse
import textwrap
from typing import Any

from scripts.tweaks_manager import TweaksManager


class ArgumentsDefiner:
    def __init__(self, colors: dict[str, Any]):
        self._parser = argparse.ArgumentParser(prog="python install.py",
                                               formatter_class=argparse.RawDescriptionHelpFormatter,
                                               epilog=self._get_epilog())

        self._define_default_arguments()
        self._define_color_arguments(colors)
        self._define_custom_color_arguments()
        self._define_theme_styles_arguments()
        self._define_color_tweaks_arguments()
        self._define_gdm_arguments()
        self._define_tweaks_arguments()

    def parse(self) -> argparse.Namespace:
        return self._parser.parse_args()

    @staticmethod
    def _get_epilog():
        return textwrap.dedent('''
                    Examples:
                      -a                            all accent colors, light & dark mode
                      --all --mode dark             all accent colors, dark mode
                      --purple --mode=light         purple accent color, light mode
                      --hue 150 --name coldgreen    custom coldgreen accent color, light & dark mode
                      --red --green --sat=70        red, green accent colors, 70% of stock saturation
                      --hue=200 --name=grayblue --sat=50 --mode=dark
                                    custom grayblue accent color, 50% of stock saturation, dark mode
                    ''')

    def _define_default_arguments(self):
        self._parser.add_argument('-r', '--remove', action='store_true', help='remove Marble themes')
        self._parser.add_argument('-ri', '--reinstall', action='store_true', help='reinstall Marble themes')

    def _define_color_arguments(self, colors: dict[str, Any]):
        default_args = self._parser.add_argument_group('Install default theme')
        default_args.add_argument('-a', '--all', action='store_true', help='all available accent colors')

        for color in colors:
            default_args.add_argument(f'--{color}', action='store_true', help=f'{color} theme only')

    def _define_custom_color_arguments(self):
        custom_args = self._parser.add_argument_group('Install custom color theme')
        custom_args.add_argument('--hue', type=int, choices=range(0, 361), help='generate theme from Hue prompt',
                                 metavar='(0 - 360)')
        custom_args.add_argument('--name', nargs='?', help='theme name (optional)')

    def _define_theme_styles_arguments(self):
        color_styles = self._parser.add_argument_group("Theme color styles")
        color_styles.add_argument("--filled", action="store_true", help="make accent color more vibrant")

    def _define_color_tweaks_arguments(self):
        color_tweaks = self._parser.add_argument_group('Optional theme tweaks')
        color_tweaks.add_argument('--mode', choices=['light', 'dark'], help='select a specific theme mode to install')
        color_tweaks.add_argument('--sat', type=int, choices=range(0, 251),
                                  help='custom color saturation (<100%% - reduce, >100%% - increase)',
                                  metavar='(0 - 250)')

    def _define_gdm_arguments(self):
        gdm_theming = self._parser.add_argument_group('GDM theming')
        gdm_theming.add_argument('--gdm', action='store_true', help='install GDM theme. \
                                            Requires root privileges. You must specify a specific color.')

    def _define_tweaks_arguments(self):
        tweaks_manager = TweaksManager()
        tweaks_manager.define_arguments(self._parser)