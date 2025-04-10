class ThemePathProvider:
    @staticmethod
    def get_theme_path(themes_folder: str, path_name: str, theme_mode: str, theme_type: str) -> str:
        return f"{themes_folder}/Marble-{path_name}-{theme_mode}/{theme_type}/"
