import os
from . import config  # name of folders and files


def generate_file(folder, final_file):
    """
    Combines all files in a folder into a single file
    :param folder: source folder
    :param final_file: location where file will be created
    """

    opened_file = open(final_file, "w")

    for file in os.listdir(folder):
        with open(folder + file) as f:
            opened_file.write(f.read() + '\n')

    opened_file.close()


def concatenate_files(edit_file, file):
    """
    Merge two files
    :param edit_file: where it will be appended
    :param file: file you want to append
    """

    with open(file, 'r') as read_file:
        file_content = read_file.read()

    with open(edit_file, 'a') as write_file:
        write_file.write('\n' + file_content)


def remove_files():
    """
    Delete already installed Marble theme
    """

    paths = (config.themes_folder, "~/.local/share/themes")

    print("💡 You do not need to delete files if you want to update theme.\n")

    confirmation = input(f"Do you want to delete all \"Marble\" folders in {' and in '.join(paths)}? (y/N) ").lower()

    if confirmation == "y":
        for path in paths:

            # Check if the path exists
            if os.path.exists(os.path.expanduser(path)):

                # Get the list of folders in the path
                folders = os.listdir(os.path.expanduser(path))

                # toggle if folder has no marble theme
                found_folder = False

                for folder in folders:
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


def destination_return(themes_folder, path_name, theme_mode, theme_type):
    """
    Copied/modified theme location
    :param themes_folder: themes folder location
    :param path_name: color name
    :param theme_mode: theme name (light or dark)
    :param theme_type: theme type (gnome-shell, gtk-4.0, ...)
    :return: copied files' folder location
    """

    return f"{themes_folder}/Marble-{path_name}-{theme_mode}/{theme_type}/"


def copy_files(source, destination):
    """
    Copy files from the source to another directory
    :param source: where files will be copied
    :param destination: where files will be pasted
    """

    destination = os.path.expanduser(destination)  # expand ~ to /home/user
    os.makedirs(destination, exist_ok=True)
    os.system(f"cp -aT {source} {destination}")


def replace_keywords(file, *args):
    """
    Replace file with several keywords
    :param file: file name where keywords must be replaced
    :param args: (keyword, replacement), (...), ...
    """

    # skip binary files in project
    if not file.lower().endswith(('.css', '.scss', '.svg')):
        return

    with open(file, "r") as read_file:
        content = read_file.read()

    for keyword, replacement in args:
        content = content.replace(keyword, replacement)

    with open(file, "w") as write_file:
        write_file.write(content)


def hex_to_rgba(hex_color):
    """
    Convert hex(a) to rgba
    :param hex_color: input value
    """

    try:
        if len(hex_color) in range(6, 10):
            hex_color = hex_color.lstrip('#') + "ff"
            # if is convertable
            int(hex_color[:], 16)
        else:
            raise ValueError

    except ValueError:
        raise ValueError(f'Error: Invalid HEX color code: {hex_color}')

    else:
        return int(hex_color[0:2], 16), \
            int(hex_color[2:4], 16), \
            int(hex_color[4:6], 16), \
            int(hex_color[6:8], 16) / 255
