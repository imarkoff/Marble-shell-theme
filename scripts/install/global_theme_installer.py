from scripts.install.theme_installer import ThemeInstaller
from scripts.utils.global_theme.gdm import GDMTheme
from scripts.utils.global_theme.gdm_builder import GDMThemeBuilder
from scripts.utils.logger.console import Console, Color, Format


class GlobalThemeInstaller(ThemeInstaller):
    theme: GDMTheme

    def remove(self):
        gdm_rm_status = self.theme.remove()
        if gdm_rm_status == 0:
            print("GDM theme removed successfully.")

    def _define_theme(self):
        gdm_builder = GDMThemeBuilder(self.colors)
        gdm_builder.with_mode(self.args.mode)
        gdm_builder.with_filled(self.args.filled)
        self.theme = gdm_builder.build()

    def _apply_tweaks_to_theme(self):
        for theme in self.theme.themes:
            self._apply_tweaks(theme.theme)

    def _after_install(self):
        print()
        Console.Line().update(
            Console.format("GDM theme installed successfully.", color=Color.GREEN, format_type=Format.BOLD),
            icon="🥳"
        )
        Console.Line().update("You need to restart GDM to apply changes.", icon="ℹ️ ")

        formatted_command = Console.format("systemctl restart gdm.service", color=Color.YELLOW, format_type=Format.BOLD)
        Console.Line().update(f"Run {formatted_command} to restart GDM.", icon="🔄")