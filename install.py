# This file installs Marble shell theme for GNOME DE
# Copyright (C) 2023-2025  Vladyslav Hroshev
import os
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import shutil

from scripts import config
from scripts.install import ArgumentsDefiner
from scripts.install.colors_definer import ColorsDefiner
from scripts.install.global_theme_installer import GlobalThemeInstaller
from scripts.install.local_theme_installer import LocalThemeInstaller
from scripts.utils.gnome import apply_gnome_theme
from scripts.utils.logger.console import Console


def main():
    colors_definer = ColorsDefiner(config.colors_json)
    args = ArgumentsDefiner(colors_definer.colors).parse()

    installer_class = GlobalThemeInstaller if args.gdm else LocalThemeInstaller
    installer = installer_class(args, colors_definer)

    if args.gdm:
        if os.getuid() != 0:
            Console().Line().error(
                "Global installation requires root privileges. Please run the script as root.")
            return

    if args.remove or args.reinstall:
        installer.remove()

    if not args.remove:
        installer.install()

    if not args.gdm and not args.remove:
        apply_gnome_theme()


if __name__ == "__main__":
    try:
        main()
    finally:
        shutil.rmtree(config.temp_folder, ignore_errors=True)