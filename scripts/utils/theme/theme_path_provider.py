import os


class ThemePathProvider:
    @staticmethod
    def get_theme_path(themes_folder: str, color_name: str, theme_mode: str, theme_type: str) -> str:
        """
        Generates the path for the theme based on the provided parameters.
        :param themes_folder: The base folder where themes are stored.
        :param color_name: The name of the color scheme.
        :param theme_mode: The mode of the theme (e.g., 'light' or 'dark').
        :param theme_type: The type of the theme (e.g., 'gnome-shell', 'gtk').
        """
        if not themes_folder or not color_name or not theme_mode or not theme_type:
            raise ValueError("All parameters must be non-empty strings.")

        marble_name = '-'.join(["Marble", color_name, theme_mode])
        final_path = os.path.join(themes_folder, marble_name, theme_type, "")

        return final_path
