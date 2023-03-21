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


import colorsys
import os
import json
import argparse
import textwrap


def generate_file(folder, final_file):
    """
    Combines all files in a folder into a single file
    :param folder: source folder
    :param final_file: location where file will be created
    """

    opened_file = open(final_file, "w")

    for file in os.listdir(folder):
        opened_file.write(open(folder + file).read() + '\n')

    opened_file.close()


def concatenate_files(file, edit_file):
    open(edit_file, 'a').write('\n' + open(file).read())


def remove_files():
    # Define the paths of the folders to be deleted
    paths = ["~/.themes", "~/.local/share/themes"]

    # Ask for confirmation before deleting
    confirmation = input(f"Do you want to delete all \"Marble\" folders in {' and in '.join(paths)}? (y/N) ")

    # If the user confirms, delete the folder
    if confirmation == "y":

        # Loop through the paths
        for path in paths:

            # Check if the path exists
            if os.path.exists(os.path.expanduser(path)):

                # Get the list of folders in the path
                folders = os.listdir(os.path.expanduser(path))

                # Loop through the folders
                found_folder = False

                # Loop through the folders
                for folder in folders:

                    # Check if the folder starts with "Marble"
                    if folder.startswith("Marble"):
                        folder_path = os.path.join(os.path.expanduser(path), folder)
                        print(f"Deleting folder {folder_path}...", end='')

                        try:
                            os.system(f"rm -r {folder_path}")

                        except Exception as e:
                            print(f"Error deleting folder {folder_path}: {e}")

                        else:
                            found_folder = True
                            print("Done.")

                if not found_folder:
                    print(f"No folders starting with \"Marble\" found in {path}.")

            else:
                print(f"The path {path} does not exist.")


def destination_return(path_name, theme_mode):
    """
    Copied/modified gnome-shell theme location
    :param path_name: color name
    :param theme_mode: theme name (light or dark)
    :return: copied files' folder location
    """

    return f"~/.themes/Marble-{path_name}-{theme_mode}/gnome-shell"


def copy_files(source, destination):
    """
    Copy files from the source to another directory
    :param source: where files will be copied
    :param destination: where files will be pasted
    """

    destination_dirs = destination.split("/")
    loop_create_dirs = f"{destination_dirs[0]}/"

    # create necessary folders
    for i in range(1, len(destination_dirs)):
        loop_create_dirs += f"{destination_dirs[i]}/"
        os.system(f"mkdir -p {loop_create_dirs}")

    os.system(f"cp -aT {source} {destination}")


def apply_colors(hue, destination, theme_mode, apply_file, sat=None):
    """
    Install accent colors from colors.json to different file
    :param hue
    :param destination: file directory
    :param theme_mode: theme name (light or dark)
    :param apply_file: file name
    :param sat: color saturation (optional)
    """

    with open(os.path.expanduser(f"{destination}/{apply_file}"), "r") as file:
        edit_file = file.read()

        # colorsys works in range(0, 1)
        h = hue / 360
        for element in colors["elements"]:
            # convert to range(0, 1)
            lightness = int(colors["elements"][element][theme_mode]["l"]) / 100
            saturation = int(colors["elements"][element][theme_mode]["s"]) / 100 if sat is None else int(
                colors["elements"][element][theme_mode]["s"]) * (sat / 100) / 100
            alpha = colors["elements"][element][theme_mode]["a"]

            # convert hsl to rgb and multiple every item
            red, green, blue = [int(item * 256) for item in colorsys.hls_to_rgb(h, lightness, saturation)]

            replace_keyword = colors["elements"][element]["replace"]

            edit_file = edit_file.replace(replace_keyword, f"rgba({red}, {green}, {blue}, {alpha})")

    with open(os.path.expanduser(f"{destination}/{apply_file}"), "w") as file:
        file.write(edit_file)


def apply_theme(hue, destination, theme_mode, sat=None):
    """
    Apply theme to all files listed in "apply-theme-files" (colors.json)
    :param hue
    :param destination: file directory
    :param theme_mode: theme name (light or dark)
    :param sat: color saturation (optional)
    """

    for apply_file in os.listdir("./gnome-shell/"):
        apply_colors(hue, destination, theme_mode, apply_file, sat=sat)


def install_color(hue, name, theme_mode, sat=None):
    """
    Copy files and generate theme with different accent color
    :param hue
    :param name: theme name
    :param theme_mode: light or dark mode
    :param sat: color saturation (optional)
    """

    print(f"Creating {name} {', '.join(theme_mode)} theme...", end=" ")

    try:
        for mode in theme_mode:
            copy_files("./gnome-shell", destination_return(name, mode))

            apply_theme(hue, destination_return(name, mode), mode, sat=sat)

    except Exception as err:
        print("\nError: " + str(err))

    else:
        print("Done.")


def hex_to_rgba(hex_color):
    """
    Convert hex(a) to rgba
    :param hex_color: input value
    """

    try:
        if len(hex_color) in range(6, 10):
            hex_color = hex_color.lstrip('#') + "ff"
            # is convertable
            int(hex_color[:], 16)
        else:
            raise ValueError
        
    except ValueError:
        raise ValueError(f'Error: Invalid HEX color code: {hex_color}')

    else:
        return int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16), int(hex_color[6:8], 16) / 255


def main():
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

    # Add default arguments
    parser.add_argument('-r', '--remove', action='store_true', help='remove all "Marble" themes')

    # Add arguments for default accent colors
    default_args = parser.add_argument_group('Install default theme')
    default_args.add_argument('-a', '--all', action='store_true', help='all available accent colors')
    default_args.add_argument('--red', action='store_true', help='red theme only')
    default_args.add_argument('--pink', action='store_true', help='pink theme only')
    default_args.add_argument('--purple', action='store_true', help='purple theme only')
    default_args.add_argument('--blue', action='store_true', help='blue theme only')
    default_args.add_argument('--green', action='store_true', help='green theme only')
    default_args.add_argument('--yellow', action='store_true', help='yellow theme only')
    default_args.add_argument('--gray', action='store_true', help='gray theme only')

    # Add arguments for custom accent colors
    custom_args = parser.add_argument_group('Install custom color theme')
    custom_args.add_argument('--hue', type=int, choices=range(0, 361), help='generate theme from Hue prompt',
                             metavar='(0 - 360)')
    custom_args.add_argument('--name', nargs='?', help='theme name (optional)')

    # Add arguments for optional theme tweaks
    color_tweaks = parser.add_argument_group('Optional theme tweaks')
    color_tweaks.add_argument('--mode', choices=['light', 'dark'], help='select a specific theme mode to install')
    color_tweaks.add_argument('--sat', type=int, choices=range(0, 251),
                              help='custom color saturation (<100%% - reduce, >100%% - increase)', metavar='(0 - 250)%')

    # Add arguments for panel tweaks
    panel_args = parser.add_argument_group('Panel tweaks')
    panel_args.add_argument('-Pds', '--panel_default_size', action='store_true', help='set default panel size')
    panel_args.add_argument('-Pnp', '--panel_no_pill', action='store_true', help='remove panel button background')
    panel_args.add_argument('-Ptc', '--panel_text_color', type=str, nargs='?', help='custom panel HEX(A) text color')
    
    args = parser.parse_args()

    mode = [args.mode] if args.mode else ['light', 'dark']

    generate_file("./css/", gnome_shell_css)

    if args.panel_default_size:
        concatenate_files("./tweaks/panel/def-size.css", gnome_shell_css)

    if args.panel_no_pill:
        concatenate_files("./tweaks/panel/no-pill.css", gnome_shell_css)

    if args.panel_text_color:
        open('./gnome-shell/gnome-shell.css', 'a') \
            .write(".panel-button,\
                    .clock,\
                    .clock-display StIcon {\
                        color: rgba(" + ', '.join(map(str, hex_to_rgba(args.panel_text_color))) + ");\
                    }")

    # Process the arguments and perform the installation accordingly
    if args.remove:
        remove_files()

    elif args.all:
        # install hue colors listed in colors.json
        for color in colors["colors"]:
            hue = colors["colors"][color]["h"]
            sat = colors["colors"][color]["s"] if colors["colors"][color]["s"] is not None else args.sat

            install_color(hue, color, mode, sat)

    elif args.red or args.pink or args.purple or args.blue or args.green or args.yellow or args.gray:
        for color_name in colors["colors"]:
            if getattr(args, color_name):
                hue = colors["colors"][color_name]["h"]
                sat = colors["colors"][color_name]["s"] if colors["colors"][color_name]["s"] is not None else args.sat

                install_color(hue, color_name, mode, sat)

    elif args.hue:
        hue = args.hue
        theme_name = args.name if args.name else f'hue{hue}'

        install_color(hue, theme_name, mode, args.sat)

    else:
        print('No arguments specified. Use -h or --help to see the available options.')


if __name__ == "__main__":
    gnome_shell_css = "./gnome-shell/gnome-shell.css"
    colors = json.load(open("colors.json"))  # used as database for replacing colors

    main()

    os.remove(gnome_shell_css)
