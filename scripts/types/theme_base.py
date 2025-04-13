from abc import ABC, abstractmethod


class ThemeBase(ABC):
    """Base class for theme installation and preparation."""
    @abstractmethod
    def prepare(self):
        pass

    @abstractmethod
    def install(self, hue: int, name: str, sat: float | None = None):
        pass