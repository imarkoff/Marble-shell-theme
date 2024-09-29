# This file installs Marble shell theme for GNOME DE
# Copyright (C) 2023-2024  Vladyslav Hroshev

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# TODO: output current GNOME version. Warn if it's not supported
# TODO: rework checkboxes for GNOME 47
# TODO: test on older GNOME versions
# TODO: install theme using only standard colors from settings color picker

import json       # working with json files
import argparse   # command-line options
import shutil
import textwrap   # example text in argparse

from scripts import config  # folder and files definitions
from scripts.tweaks_manager import TweaksManager  # load tweaks from files

from scripts.utils import remove_files  # delete already installed Marble theme
from scripts.utils.gnome import apply_gnome_theme  # apply theme to GNOME shell

from scripts.theme import Theme
from scripts.gdm import GlobalTheme


def parse_args(colors):
    """
    Parse command-line arguments
    :return: parsed arguments
    """

    # script description
    parser = argparse.ArgumentParser(prog="python install.py",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=textwrap.dedent('''
                    Examples:
                      -a                            all accent colors, light & dark mode
                      --all --mode dark             all accent colors, dark mode
                      --purple --mode=light         purple accent color, light mode
                      --hue 150 --name coldgreen    custom coldgreen accent color, light & dark mode
                      --red --green --sat=70        red, green accent colors, 70% of stock saturation
                      --hue=200 --name=grayblue --sat=50 --mode=dark
                                    custom grayblue accent color, 50% of stock saturation, dark mode
                    '''))

    # Default arguments
    parser.add_argument('-r', '--remove', action='store_true', help='remove all "Marble" themes')

    default_args = parser.add_argument_group('Install default theme')
    default_args.add_argument('-a', '--all', action='store_true', help='all available accent colors')

    for color in colors["colors"]:
        default_args.add_argument(f'--{color}', action='store_true', help=f'{color} theme only')

    custom_args = parser.add_argument_group('Install custom color theme')
    custom_args.add_argument('--hue', type=int, choices=range(0, 361), help='generate theme from Hue prompt',
                             metavar='(0 - 360)')
    custom_args.add_argument('--name', nargs='?', help='theme name (optional)')

    color_styles = parser.add_argument_group("Theme color tweaks")
    color_styles.add_argument("--filled", action="store_true", help="make accent color more vibrant")

    color_tweaks = parser.add_argument_group('Optional theme tweaks')
    color_tweaks.add_argument('--mode', choices=['light', 'dark'], help='select a specific theme mode to install')
    color_tweaks.add_argument('--sat', type=int, choices=range(0, 251),
                              help='custom color saturation (<100%% - reduce, >100%% - increase)', metavar='(0 - 250)%')

    gdm_theming = parser.add_argument_group('GDM theming')
    gdm_theming.add_argument('--gdm', action='store_true', help='install GDM theme. \
                                    Requires root privileges. You must specify a specific color.')

    # Dynamically load arguments from each tweak script
    tweaks_manager = TweaksManager()
    tweaks_manager.define_arguments(parser)

    return parser.parse_args()


def apply_tweaks(args, theme, colors):
    """
    Apply theme tweaks
    :param args: parsed arguments
    :param theme: Theme object
    :param colors: colors from colors.json
    """

    tweaks_manager = TweaksManager()
    tweaks_manager.apply_tweaks(args, theme, colors)


def install_theme(theme, hue, theme_name, sat, gdm=False):
    """
    Check if GDM and install theme
    :param theme: object to install
    :param hue: color hue
    :param theme_name: future theme name
    :param sat: color saturation
    :param gdm: if GDM theme
    """

    if gdm:
        theme.install(hue, sat)
    else:
        theme.install(hue, theme_name, sat)


def apply_colors(args, theme, colors, gdm=False):
    """
    Apply accent colors to the theme
    :param args: parsed arguments
    :param theme: Theme object
    :param colors: colors from colors.json
    :param gdm: if GDM theme
    """

    is_colors = False  # check if any color arguments specified

    # if custom color
    if args.hue:
        hue = args.hue
        theme_name = args.name if args.name else f'hue{hue}'

        install_theme(theme, hue, theme_name, args.sat, gdm)
        return

    else:
        for color in colors["colors"]:
            if args.all or getattr(args, color):
                is_colors = True

                hue = colors["colors"][color]["h"]
                # if saturation already defined in color (gray)
                sat = colors["colors"][color].get("s", args.sat)

                install_theme(theme, hue, color, sat, gdm)
                if gdm:
                    return

    if not is_colors:
        print('No color arguments specified. Use -h or --help to see the available options.')


def global_theme(args, colors):
    """
    Apply GDM theme
    :param args: parsed arguments
    :param colors: colors from colors.json
    """

    gdm_theme = GlobalTheme(colors, f"{config.raw_theme_folder}/{config.gnome_folder}",
                            config.global_gnome_shell_theme, config.gnome_shell_gresource,
                            config.temp_folder, is_filled=args.filled)

    if args.remove:
        gdm_rm_status = gdm_theme.remove()
        if gdm_rm_status == 0:
            print("GDM theme removed successfully.")
        return 0

    try:
        apply_colors(args, gdm_theme, colors, gdm=True)
    except Exception as e:
        print(f"Error: {e}")
        return 1
    else:
        print("\nGDM theme installed successfully.")
        print("You need to restart gdm.service to apply changes.")
        print("Run \"systemctl restart gdm.service\" to restart GDM.")


def local_theme(args, colors):
    """
    Apply local theme
    :param args: parsed arguments
    :param colors: colors from colors.json
    """

    if args.remove:
        remove_files()

    gnome_shell_theme = Theme("gnome-shell", colors, f"{config.raw_theme_folder}/{config.gnome_folder}",
                              config.themes_folder, config.temp_folder,
                              mode=args.mode, is_filled=args.filled)

    apply_tweaks(args, gnome_shell_theme, colors)
    apply_colors(args, gnome_shell_theme, colors)


def main():
    colors = json.load(open(config.colors_json))

    args = parse_args(colors)

    if args.gdm:
        global_theme(args, colors)

    else:
        local_theme(args, colors)
        apply_gnome_theme()
        # TODO: inform user about already applied theme. if not, apply it manually


if __name__ == "__main__":
    main()

    shutil.rmtree(config.temp_folder, ignore_errors=True)
