import os

def get_version_folders(version, base_path):
    """
    Get version folders
    :param version: gnome-shell version
    :param base_path: base path to version folders
    :return: list of matching version folders
    """
    version_folders = os.listdir(base_path)
    version = int(version.split('.')[0])  # Use only the major version for comparison
    matching_folders = []

    for folder in version_folders:
        if '..' in folder:
            from_version, to_version = folder.split('..')
            if from_version and to_version:
                if int(from_version) <= version <= int(to_version):
                    matching_folders.append(folder)
            elif from_version:
                if version >= int(from_version):
                    matching_folders.append(folder)
            elif to_version:
                if version <= int(to_version):
                    matching_folders.append(folder)
        elif int(folder) == version:
            matching_folders.append(folder)

    return matching_folders