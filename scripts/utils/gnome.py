import subprocess

def gnome_version():
    """
    Get gnome-shell version
    """

    try:
        output = subprocess.check_output(['gnome-shell', '--version'], text=True).strip()
        return output.split(' ')[2]
    except subprocess.CalledProcessError:
        return None

def apply_gnome_theme(theme=None):
    """
    Apply gnome-shell theme
    :param theme: theme name
    """

    try:
        if theme is None:
            current_theme = subprocess.check_output(['dconf', 'read', '/org/gnome/shell/extensions/user-theme/name'], text=True).strip().strip("'")
            if current_theme.startswith("Marble"):
                theme = current_theme
            else:
                return False

        subprocess.run(['dconf', 'reset', '/org/gnome/shell/extensions/user-theme/name'], check=True)
        subprocess.run(['dconf', 'write', '/org/gnome/shell/extensions/user-theme/name', f"'{theme}'"], check=True)
    except subprocess.CalledProcessError:
        return False
    return True