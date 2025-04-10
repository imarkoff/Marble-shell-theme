import colorsys
from abc import ABC, abstractmethod


class ColorConverter(ABC):
    @staticmethod
    @abstractmethod
    def hex_to_rgba(hex_color):
        pass

    @staticmethod
    @abstractmethod
    def hsl_to_rgb(hue, saturation, lightness):
        pass


class ColorConverterImpl(ColorConverter):
    @staticmethod
    def hex_to_rgba(hex_color):
        try:
            if len(hex_color) in range(6, 10):
                hex_color = hex_color.lstrip('#') + "ff"
                # if is convertable
                int(hex_color[:], 16)
            else:
                raise ValueError

        except ValueError:
            raise ValueError(f'Error: Invalid HEX color code: {hex_color}')

        else:
            return int(hex_color[0:2], 16), \
                int(hex_color[2:4], 16), \
                int(hex_color[4:6], 16), \
                int(hex_color[6:8], 16) / 255

    @staticmethod
    def hsl_to_rgb(hue, saturation, lightness):
        # colorsys works in range(0, 1)
        h = hue / 360
        red, green, blue = [int(item * 255) for item in colorsys.hls_to_rgb(h, lightness, saturation)]
        return red, green, blue