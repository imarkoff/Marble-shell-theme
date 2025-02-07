def destination_return(themes_folder, path_name, theme_mode, theme_type):
    """
    Copied/modified theme location
    :param themes_folder: themes folder location
    :param path_name: color name
    :param theme_mode: theme name (light or dark)
    :param theme_type: theme type (gnome-shell, gtk-4.0, ...)
    :return: copied files' folder location
    """

    return f"{themes_folder}/Marble-{path_name}-{theme_mode}/{theme_type}/"
