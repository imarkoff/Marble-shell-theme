# TODO: Add ability to delete custom colors
# TODO: Create an interface where the user can select which themes to delete
# TODO: Add a flag to skip the confirmation prompt

import argparse
import shutil
from collections import defaultdict
from typing import Any

from scripts.utils.logger.console import Console, Color, Format
from .parse_folder import parse_folder
from .. import config
import os

def remove_files(args: argparse.Namespace, formatted_colors: dict[str, Any]):
    """Delete already installed Marble theme"""
    themes = detect_themes(config.themes_folder)

    filtered_themes = themes

    if args.all:
        filtered_themes = themes
    if not args.all:
        args_dict = vars(args)
        arguments = [color for color in formatted_colors.keys() if args_dict.get(color)]
        filtered_themes = themes.filter(arguments)

    if not filtered_themes:
        Console.Line().error("No matching themes found.")
        return

    formatted_colors = [
        Console.format(color, color=Color.get(color), format_type=Format.BOLD)
        for (color, modes) in filtered_themes
    ]
    Console.Line().warn(f"The following themes will be deleted: {', '.join(formatted_colors)}.")
    if args.mode:
        Console.Line().warn(f"Theme modes to be deleted: {args.mode}.")

    if proceed_input().lower() == "y":
        filtered_themes.remove(args.mode)
        Console.Line().success("Themes deleted successfully.")
    else:
        Console.Line().error("Operation cancelled.")


def detect_themes(path: str) -> 'Themes':
    """Detect themes in a given path"""
    abs_path = os.path.expanduser(path)
    themes = Themes()

    if not os.path.exists(abs_path):
        return themes

    folders = os.listdir(abs_path)

    for folder in folders:
        parsed = parse_folder(folder)
        if parsed:
            (color, mode) = parsed
            theme_mode = ThemeMode(mode=mode, path=os.path.join(abs_path, folder))
            themes.add_theme(color, theme_mode)

    return themes


class Themes:
    """Collection of themes grouped by color"""
    def __init__(self):
        self.by_color: dict[str, list[ThemeMode]] = defaultdict(list)  # color: list[ThemeMode]

    def add_theme(self, color: str, theme_mode: 'ThemeMode'):
        self.by_color[color].append(theme_mode)

    def filter(self, colors: list[str]):
        """
        Filter themes by colors.
        Returns a new Themes object.
        """
        filtered = Themes()

        for color in colors:
            if color in self.by_color:
                filtered.by_color[color] = self.by_color[color].copy()

        return filtered

    def remove(self, mode: str | None = None):
        for modes in self.by_color.values():
            for theme_mode in modes:
                if mode is None or theme_mode.mode == mode:
                    theme_mode.remove()

    def __bool__(self):
        return bool(self.by_color)

    def __iter__(self):
        for color, modes in self.by_color.items():
            yield color, modes


class ThemeMode:
    """Concrete theme with mode and path"""
    mode: str
    path: str

    def __init__(self, mode: str, path: str):
        self.mode = mode
        self.path = path

    def remove(self):
        try:
            shutil.rmtree(self.path)
        except Exception as e:
            print(f"Error deleting {self.path}: {e}")


def proceed_input():
    formatted_agree = Console.format("y", color=Color.GREEN, format_type=Format.BOLD)
    formatted_disagree = Console.format("N", color=Color.RED, format_type=Format.BOLD)
    formatted_proceed = Console.format("Proceed?", format_type=Format.BOLD)
    return input(f"{formatted_proceed} ({formatted_agree}/{formatted_disagree}) ")