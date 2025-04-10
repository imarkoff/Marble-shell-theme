from abc import ABC


class ThemeBase(ABC):
    """Base class for theme installation and preparation."""
    @staticmethod
    def prepare(self):
        pass

    @staticmethod
    def install(self, hue: int, sat: float | None = None):
        pass