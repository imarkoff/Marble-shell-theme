import colorsys

from scripts.utils.color_converter.color_converter import ColorConverter


class ColorConverterImpl(ColorConverter):
    @staticmethod
    def hex_to_rgba(hex_color):
        try:
            hex_color = hex_color.lstrip('#')

            # Handle shorthand hex colors (e.g., #fff)
            if len(hex_color) == 3:
                hex_color = ''.join([char * 2 for char in hex_color])

            # Add alpha channel if missing
            if len(hex_color) == 6:
                hex_color += "ff"

            # Validate the hex color
            int(hex_color, 16)

        except ValueError:
            raise ValueError(f'Error: Invalid HEX color code: #{hex_color}')

        else:
            return int(hex_color[0:2], 16), \
                int(hex_color[2:4], 16), \
                int(hex_color[4:6], 16), \
                int(hex_color[6:8], 16) / 255

    @staticmethod
    def hsl_to_rgb(hue, saturation, lightness):
        if hue > 360 or hue < 0:
            raise ValueError(f'Hue must be between 0 and 360, not {hue}')
        if saturation > 1 or saturation < 0:
            raise ValueError(f'Saturation must be between 0 and 1, not {saturation}')
        if lightness > 1 or lightness < 0:
            raise ValueError(f'Lightness must be between 0 and 1, not {lightness}')

        h = hue / 360
        red, green, blue = [round(item * 255) for item in colorsys.hls_to_rgb(h, lightness, saturation)]
        return red, green, blue
