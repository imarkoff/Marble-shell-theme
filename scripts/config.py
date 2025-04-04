import os.path
from tempfile import gettempdir

# folder definitions
temp_folder = f"{gettempdir()}/marble"
gdm_folder = "gdm"
gnome_folder = "gnome-shell"
temp_gnome_folder = f"{temp_folder}/{gnome_folder}"
tweaks_folder = "tweaks"
themes_folder = "~/.themes"
raw_theme_folder = "theme"
scripts_folder = "scripts"

# GDM definitions
global_gnome_shell_theme = "/usr/share/gnome-shell"
gnome_shell_gresource = "gnome-shell-theme.gresource"
ubuntu_gresource_link = "gtk-theme.gresource"
extracted_gdm_folder = "theme"

# files definitions
gnome_shell_css = f"{temp_gnome_folder}/gnome-shell.css"
tweak_file = f"./{tweaks_folder}/*/tweak.py"
colors_json = "colors.json"

user_themes_extension = "/org/gnome/shell/extensions/user-theme/name"
