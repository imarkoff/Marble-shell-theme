import os


def create_dummy_file(file_path: str, content: str = "dummy content"):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(content)


def try_remove_file(file_path: str):
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass