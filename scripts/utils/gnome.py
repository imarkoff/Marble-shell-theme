import subprocess
import time

from scripts import config
from scripts.utils.logger.console import Console, Format, Color
from scripts.utils.parse_folder import parse_folder


def gnome_version() -> str | None:
    """
    Get gnome-shell version
    """
    try:
        output = subprocess.check_output(['gnome-shell', '--version'], text=True).strip()
        return output.split(' ')[2]
    except subprocess.CalledProcessError:
        return None

def apply_gnome_theme(theme=None) -> bool:
    """
    Applies the theme in user theme extension if it is Marble and extension installed.
    """
    try:
        if theme is None:
            theme = get_current_theme()

        line = Console.Line("apply_gnome_theme")
        (color, _) = parse_folder(theme)
        formatted_theme = Console.format(theme, color=Color.get(color, Color.GRAY), format_type=Format.BOLD)

        line.update(f"Applying {formatted_theme} theme...")
        time.sleep(0.025) # applying the theme may freeze, so we need to wait a bit
        apply_user_theme(theme)
        line.success(f"Theme {formatted_theme} applied.")
    except Exception:
        return False
    return True


def get_current_theme() -> str:
    """
    Throws an error if theme is not Marble.
    """
    try:
        output = subprocess.check_output(['dconf', 'read', config.user_themes_extension], text=True)
        output = output.strip().strip("'")

        if not output.startswith("Marble"):
            raise Exception(f"Theme {output} doesn't appear to be a Marble theme")
        return output
    except subprocess.CalledProcessError:
        raise Exception("User theme extension not found.")


def apply_user_theme(theme_name: str):
    subprocess.run(['dconf', 'reset', config.user_themes_extension], check=True)
    subprocess.run(['dconf', 'write', config.user_themes_extension, f"'{theme_name}'"], check=True)