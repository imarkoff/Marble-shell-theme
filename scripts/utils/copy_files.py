import os

def copy_files(source, destination):
    """
    Copy files from the source to another directory
    :param source: where files will be copied
    :param destination: where files will be pasted
    """

    destination = os.path.expanduser(destination)  # expand ~ to /home/user
    os.makedirs(destination, exist_ok=True)
    os.system(f"cp -aT {source} {destination}")
