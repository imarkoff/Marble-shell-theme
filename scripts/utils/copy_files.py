import os
import shutil


def copy_files(source, destination):
    """
    Copy files from the source to another directory
    :param source: where files will be copied
    :param destination: where files will be pasted
    """

    destination = os.path.expanduser(destination)
    os.makedirs(destination, exist_ok=True)

    shutil.copytree(source, destination, dirs_exist_ok=True)
