from scripts.install.theme_installer import ThemeInstaller
from scripts.utils.theme.gnome_shell_theme_builder import GnomeShellThemeBuilder
from scripts.utils.theme.theme import Theme
from scripts.utils import remove_files
from scripts.utils.logger.console import Console, Color, Format


class LocalThemeInstaller(ThemeInstaller):
    theme: Theme

    def remove(self):
        colors = self.colors.colors
        remove_files(self.args, colors)

    def _define_theme(self):
        theme_builder = GnomeShellThemeBuilder(self.colors)
        theme_builder.with_mode(self.args.mode)
        theme_builder.filled(self.args.filled)
        self.theme = theme_builder.build()

    def _apply_tweaks_to_theme(self):
        self._apply_tweaks(self.theme)

    def _after_install(self):
        print()
        formatted_output = Console.format("Theme installed successfully.", color=Color.GREEN, format_type=Format.BOLD)
        Console.Line().update(formatted_output, icon="🥳")