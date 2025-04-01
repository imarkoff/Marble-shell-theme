def parse_folder(folder: str) -> tuple[str, str] | None:
    """Parse a folder name into color and mode"""
    folder_arr = folder.split("-")

    if len(folder_arr) < 2 or folder_arr[0] != "Marble":
        return None

    color = "-".join(folder_arr[1:-1])
    mode = folder_arr[-1]

    return color, mode