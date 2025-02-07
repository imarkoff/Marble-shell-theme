def hex_to_rgba(hex_color):
    """
    Convert hex(a) to rgba
    :param hex_color: input value
    """

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