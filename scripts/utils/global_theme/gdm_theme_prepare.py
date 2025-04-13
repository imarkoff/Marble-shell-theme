from scripts.utils import remove_keywords, remove_properties
from scripts.utils.files_labeler import FilesLabeler
from scripts.utils.theme.theme import Theme


class GDMThemePrepare:
    """
    Prepares theme files for installation into the GDM system.

    This class handles:
    - Theme file labeling for dark/light variants
    - CSS property and keyword removal for customization
    - Theme installation with color adjustments
    """
    def __init__(self, theme: Theme, theme_file: str, label: str | None,
                 files_labeler: FilesLabeler):
        """
        :param theme: The theme object to prepare
        :param theme_file: Path to the original decompiled CSS file
        :param label: Optional label for the theme (e.g. "dark", "light")
        :param files_labeler: FilesLabeler instance for labeling files
        """
        self.theme = theme
        self.theme_file = theme_file
        self.label = label
        self.files_labeler = files_labeler

    def label_theme(self):
        """
        Label the theme files if the label is set.
        Also updates references in the theme files.
        :raises ValueError: if the label is not set
        """
        if self.label is None:
            raise ValueError("Label is not set for the theme.")

        self.files_labeler.append_label(self.label)

    def remove_keywords(self, *args: str):
        """Remove specific keywords from the theme file"""
        remove_keywords(self.theme_file, *args)

    def remove_properties(self, *args: str):
        """Remove specific properties from the theme file"""
        remove_properties(self.theme_file, *args)

    def prepend_source_styles(self, trigger: str):
        """
        Add source styles and installation trigger to the theme file.

        This adds original theme styles and a marker that identifies
        the theme as installed by this application.

        :param trigger: String marker used to identify installed themes
        """
        with open(self.theme_file, 'r') as gnome_theme:
            gnome_styles = gnome_theme.read() + '\n' + trigger + '\n'
            self.theme.add_to_start(gnome_styles)

    def install(self, hue: int, color: str, sat: int | None, destination: str):
        """
        Install the theme to the specified destination
        :param hue: Hue value for the theme
        :param color: Color name for the theme
        :param sat: Saturation value for the theme
        :param destination: Destination folder for the theme
        """
        self.theme.install(hue, color, sat, destination=destination)