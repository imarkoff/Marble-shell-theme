# TODO: Less verbose output for the user and simplify the code

from .. import config
import os

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