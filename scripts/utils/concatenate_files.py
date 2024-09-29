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