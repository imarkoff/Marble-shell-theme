import os
import shutil
from .gnome import gnome_version
from .get_version_folder import get_version_folders

def generate_file(folder, final_file):
    """
    Combines all files in a folder into a single file
    :param folder: source folder
    :param final_file: location where file will be created
    """
    opened_file = open(final_file, "w")
    css_folder = f"{folder}/.css/"

    for file in os.listdir(css_folder):
        with open(os.path.join(css_folder, file)) as f:
            opened_file.write(f.read() + '\n')

    version = gnome_version()

    if version:
        base_path = f"{folder}/.versions/"
        version_folders = get_version_folders(version, base_path)

        for version_folder in version_folders:
            version_path = os.path.join(base_path, version_folder)
            css_path = os.path.join(version_path, '.css')

            for css_file in os.listdir(css_path):
                with open(os.path.join(css_path, css_file)) as f:
                    opened_file.write(f.read() + '\n')

            for file in os.listdir(version_path):
                if file.endswith('.svg'):
                    shutil.move(os.path.join(version_path, file), folder)

    opened_file.close()