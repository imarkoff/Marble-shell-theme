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
