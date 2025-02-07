import os

def label_files(directory, label, *args):
    """
    Add a label to all files in a directory
    :param directory: folder where files are located
    :param label: label to add
    :param args: files to change links to labeled files
    :return:
    """

    # Open all files
    files = [open(file, 'r') for file in args]
    read_files = []

    filenames = []

    for filename in os.listdir(directory):
        # Skip if the file is already labeled
        if label in filename:
            continue

        # Split the filename into name and extension
        name, extension = os.path.splitext(filename)

        # Form the new filename and rename the file
        new_filename = f"{name}-{label}{extension}"
        os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))

        filenames.append((filename, new_filename))

    # Replace the filename in all files
    for i, file in enumerate(files):
        read_file = file.read()
        read_file.replace(filenames[i][0], filenames[i][1])
        read_files.append(read_file)
        file.close()

    write_files = [open(file, 'w') for file in args]

    # Write the changes to the files and close them
    for i, file in enumerate(write_files):
        file.write(read_files[i])
        file.close()
