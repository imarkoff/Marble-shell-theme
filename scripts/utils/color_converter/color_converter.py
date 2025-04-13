from abc import ABC, abstractmethod


class ColorConverter(ABC):
    @staticmethod
    @abstractmethod
    def hex_to_rgba(hex_color):
        """
        Converts a HEX color code to RGBA format.
        :param hex_color: HEX color code (e.g., '#ff5733' or 'ff5733').
        :return: Tuple of RGBA values (red, green, blue, alpha).
        :raises ValueError: If the HEX color code is invalid.
        """
        pass

    @staticmethod
    @abstractmethod
    def hsl_to_rgb(hue, saturation, lightness):
        """
        Converts HSL color values to RGB format.
        :param hue: Hue value (0-360).
        :param saturation: Saturation value (0-1).
        :param lightness: Lightness value (0-1).
        :return: Tuple of RGB values (red, green, blue) in range(0-255).
        """
        pass
