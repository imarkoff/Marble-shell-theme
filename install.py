import colorsys
import os
import json


def print_help():
    """ Print usage documentation """

    print("Default colors\n"
          "-A, --all\tInstall all available accent colors. Light & dark mode.\n"
          "--red\t\tred theme only\n"
          "--pink\t\tpink theme only\n"
          "--purple\tpurple theme only\n"
          "--blue\t\tblue theme only\n"
          "--green\t\tgreen theme only\n"
          "--yellow\tpink theme only\n"
          "--gray\t\tgray theme only")

    print("\nCustom Hue colors:\n"
          "--hue\tHUE_DEGREE\tTHEME_NAME[optional]\tTHEME_MODE[optional]\nGenerate theme from Hue prompt [0 - 360]")

    print("\nTheme mode:\n"
          "\t--light light theme only\n"
          "\t--dark  dark theme only")

    print("\nExample:\n"
          "-A\t\t\tInstall all accent colors with light & dark mode\n"
          "--all --dark\t\tInstall all accent colors with dark mode only\n"
          "--purple --light\tInstall purple accent color with light mode only\n"
          "--hue 180\t\tInstall hue=180 accent color with light & dark mode\n"
          "--hue 140 coldgreen --dark\tInstall hue=140 coldgreen accent color with dark mode only")


def destination_return(path_name, theme_mode):
    """
    Copied/modified gnome-shell theme location
    :param path_name: color name
    :param theme_mode: theme name (light or dark)
    :return: copied files' folder location
    """

    return f"~/.local/share/themes/Marble-Shell-{path_name}-{theme_mode}/gnome-shell"


def copy_files(source, destination):
    """
    Copy files from the source to another directory
    :param source: where files will be copied
    :param destination: where files will be pasted
    """

    destinationDirs = destination.split("/")
    loopCreateDirs = f"{destinationDirs[0]}/"

    for i in range(1, len(destinationDirs)):
        loopCreateDirs += f"{destinationDirs[i]}/"
        os.system(f"mkdir -p {loopCreateDirs}")

    os.system(f"cp -aT {source} {destination}")


def apply_theme_to_file(hue, destination, theme_mode, apply_file, sat=None):
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

        h = hue / 360
        for i in colors[f"{theme_mode}"]:
            lightness = int(colors[f"{theme_mode}"][i]["l"]) / 100
            saturation = int(colors[f"{theme_mode}"][i]["s"]) / 100 if sat is None else sat

            hls_to_rgb = colorsys.hls_to_rgb(h, lightness, saturation)

            edit_file = edit_file.replace(colors[f"{theme_mode}"][i]["replace"],
                                          f"rgba({int(hls_to_rgb[0] * 256)},"
                                          f"{int(hls_to_rgb[1] * 256)},"
                                          f"{int(hls_to_rgb[2] * 256)},"
                                          f"{colors[f'{theme_mode}'][i]['a']})")

    with open(os.path.expanduser(f"{destination}/{apply_file}"), "w") as file:
        file.write(edit_file)

    colorsOpen.close()


def apply_theme(hue, destination, theme_mode, sat=None):
    """
    Apply theme to all files listed in "apply-theme-files" (colors.json)
    :param hue
    :param destination: file directory
    :param theme_mode: theme name (light or dark)
    :param sat: color saturation (optional)
    """

    for applyFile in colors["apply-theme-files"]:
        apply_theme_to_file(hue, destination, theme_mode, applyFile, sat=sat)


def install_color(hue, path_name, theme_mode, sat=None):
    """
    Copy files and generate theme with different accent color
    :param hue
    :param path_name: color name
    :param theme_mode: theme name (light or dark)
    :param sat: color saturation (optional)
    """

    print(f"Creating {path_name} {theme_mode} theme...", end=" ")

    copy_files("./gnome-shell", destination_return(path_name, theme_mode))
    apply_theme(hue, destination_return(path_name, theme_mode), theme_mode, sat=sat)

    print("Done.")


def install_all(theme_mode):
    """
    Install all accent colors listed in "colors", colors.json
    :param theme_mode: theme name (light or dark)
    """
    for color in colors["colors"]:
        install_color(colors["colors"][color]["h"], color, theme_mode)
    install_color(0, "gray", theme_mode, sat=0)


def main():
    user_input = input("\n>>> ").split()
    userInputLength = len(user_input)

    match user_input[0]:
        case "-A" | "--all":
            if userInputLength == 1 or user_input[1] != "--light" and user_input[1] != "--dark":
                install_all("light")
                install_all("dark")
            else:
                install_all(user_input[1][2:len(user_input[1])])

        case "--red" | "--pink" | "--purple" | "--blue" | "--green" | "--yellow":
            path_name = user_input[0][2:len(user_input[0])]
            hue = colors["colors"][path_name]["h"]

            if userInputLength == 1 or user_input[1] != "--light" and user_input[1] != "--dark":
                install_color(hue, path_name, "light")
                install_color(hue, path_name, "dark")
            else:
                install_color(hue, path_name, user_input[1][2:len(user_input[1])])

        case "--gray" | "--grey":
            if userInputLength == 1 or user_input[1] != "--light" and user_input[1] != "--dark":
                install_color(0, "gray", "light", sat=0)
                install_color(0, "gray", "dark", sat=0)
            else:
                install_color(0, "gray", user_input[1][2:len(user_input[1])], sat=0)

        case "--hue":
            if not user_input[1].isdigit():
                print("Incorrect hue degree. It must be integer, not string.", end="")
                main()

            elif int(user_input[1]) not in range(0, 360):
                print("Incorrect hue degree. The integer must be from 0 to 360.", end="")
                main()

            elif userInputLength == 2 and user_input[2] != "--light" and user_input[2] != "--dark":
                install_color(int(user_input[1]), user_input[1], "light")
                install_color(int(user_input[1]), user_input[1], "dark")

            elif userInputLength == 2 and user_input[2] == "--light" or \
                    userInputLength == 2 and user_input[2] == "--dark":
                install_color(int(user_input[1]), user_input[1], user_input[2][2:len(user_input[2])])

            elif userInputLength == 3 or user_input[3] != "--light" and user_input[3] != "--dark":
                install_color(int(user_input[1]), user_input[2], "light")
                install_color(int(user_input[1]), user_input[2], "dark")

            elif user_input[3] == "--light" or user_input[3] == "--dark":
                install_color(int(user_input[1]), user_input[2], user_input[3][2:len(user_input[3])])


print_help()

colorsOpen = open("colors.json")
colors = json.loads(colorsOpen.read())   # used as database for replacing colors, files which must be generated

main()
