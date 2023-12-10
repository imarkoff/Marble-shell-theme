# This file installs Marble shell theme for GNOME DE
# Copyright (C) 2023  Vladyslav Hroshev

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


import json       # working with json files
import os         # system commands, working with files
import argparse   # command-line options
import shutil
import textwrap   # example text in argparse

from scripts import config     # folder and files definitions

from scripts.utils import (
    remove_files,  # delete already installed Marble theme
    hex_to_rgba)   # convert HEX to RGBA

from scripts.theme import Theme
from scripts.gdm import GlobalTheme


def main():
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
    default_args.add_argument('--red', action='store_true', help='red theme only')
    default_args.add_argument('--pink', action='store_true', help='pink theme only')
    default_args.add_argument('--purple', action='store_true', help='purple theme only')
    default_args.add_argument('--blue', action='store_true', help='blue theme only')
    default_args.add_argument('--green', action='store_true', help='green theme only')
    default_args.add_argument('--yellow', action='store_true', help='yellow theme only')
    default_args.add_argument('--gray', action='store_true', help='gray theme only')

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

    panel_args = parser.add_argument_group('Panel tweaks')
    panel_args.add_argument('-Pds', '--panel_default_size', action='store_true', help='set default panel size')
    panel_args.add_argument('-Pnp', '--panel_no_pill', action='store_true', help='remove panel button background')
    panel_args.add_argument('-Ptc', '--panel_text_color', type=str, nargs='?', help='custom panel HEX(A) text color')

    overview_args = parser.add_argument_group('Overview tweaks')
    overview_args.add_argument('--launchpad', action='store_true', help='change Show Apps icon to MacOS Launchpad icon')
    
    args = parser.parse_args()

    colors = json.load(open(config.colors_json))

    if args.gdm:
        gdm_status = 1
        if os.geteuid() != 0:
            print("You must run this script as root to install GDM theme.")
            return 1

        if args.all:
            print("Error: You can't install all colors for GDM theme. Use specific color.")
            return 1

        gdm_theme = GlobalTheme(colors, f"{config.raw_theme_folder}/{config.gnome_folder}",
                                config.global_gnome_shell_theme, config.gnome_shell_gresource,
                                config.temp_folder, is_filled=args.filled)

        if args.red or args.pink or args.purple or args.blue or args.green or args.yellow or args.gray:
            for color in colors["colors"]:
                if getattr(args, color):
                    hue = colors["colors"][color]["h"]
                    sat = colors["colors"][color]["s"] if colors["colors"][color]["s"] is not None else args.sat

                    gdm_status = gdm_theme.install(hue, sat)

        elif args.hue:
            hue = args.hue

            gdm_status = gdm_theme.install(hue, args.sat)

        else:
            print('No color arguments specified. Use -h or --help to see the available options.')

        if gdm_status == 0:
            print("\nGDM theme installed successfully.")
            print("You need to restart gdm.service to apply changes.")
            print("Run \"systemctl restart gdm.service\" to restart GDM.")

    # if not GDM theme
    else:
        # remove marble theme
        if args.remove:
            remove_files()

        gnome_shell_theme = Theme("gnome-shell", colors, f"{config.raw_theme_folder}/{config.gnome_folder}",
                                  config.themes_folder, config.temp_folder,
                                  mode=args.mode, is_filled=args.filled)

        # panel tweaks
        if args.panel_default_size:
            with open(f"{config.tweaks_folder}/panel/def-size.css", "r") as f:
                gnome_shell_theme += f.read()

        if args.panel_no_pill:
            with open(f"{config.tweaks_folder}/panel/no-pill.css", "r") as f:
                gnome_shell_theme += f.read()

        if args.panel_text_color:
            gnome_shell_theme += ".panel-button,\
                        .clock,\
                        .clock-display StIcon {\
                            color: rgba(" + ', '.join(map(str, hex_to_rgba(args.panel_text_color))) + ");\
                        }"

        # dock tweaks
        if args.launchpad:
            with open(f"{config.tweaks_folder}/launchpad/launchpad.css", "r") as f:
                gnome_shell_theme += f.read()

            gnome_shell_theme *= f"{config.tweaks_folder}/launchpad/launchpad.png"

        # what argument colors defined
        if args.all:
            # install hue colors listed in colors.json
            for color in colors["colors"]:
                hue = colors["colors"][color]["h"]
                # if saturation already defined in color (gray)
                sat = colors["colors"][color]["s"] if colors["colors"][color]["s"] is not None else args.sat

                gnome_shell_theme.install(hue, color, sat)

        elif args.red or args.pink or args.purple or args.blue or args.green or args.yellow or args.gray:
            # install selected colors
            for color in colors["colors"]:
                if getattr(args, color):  # if argument name is in defined colors
                    hue = colors["colors"][color]["h"]
                    # if saturation already defined in color (gray)
                    sat = colors["colors"][color]["s"] if colors["colors"][color]["s"] is not None else args.sat

                    gnome_shell_theme.install(hue, color, sat)

        # custom color
        elif args.hue:
            hue = args.hue
            theme_name = args.name if args.name else f'hue{hue}'  # if defined name

            gnome_shell_theme.install(hue, theme_name, args.sat)

        else:
            print('No arguments or no color arguments specified. Use -h or --help to see the available options.')


if __name__ == "__main__":
    main()

    shutil.rmtree(config.temp_folder, ignore_errors=True)
