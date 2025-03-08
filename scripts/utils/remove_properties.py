def remove_properties(file, *args):
    """
    Remove properties from a file
    :param file: file name
    :param args: properties to remove
    """

    new_content = ""

    with open(file, "r") as read_file:
        content = read_file.read()

        for line in content.splitlines():
            if not any(prop in line for prop in args):
                new_content += line + "\n"
            elif "}" in line:
                new_content += "}\n"

    with open(file, "w") as write_file:
        write_file.write(new_content)