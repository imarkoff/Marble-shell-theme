def remove_keywords(file, *args):
    """
    Remove keywords from a file
    :param file: file name
    :param args: keywords to remove
    """

    with open(file, "r") as read_file:
        content = read_file.read()

        for arg in args:
            content = content.replace(arg, "")

    with open(file, "w") as write_file:
        write_file.write(content)
