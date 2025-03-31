import json


class ColorsDefiner:
    # TODO: Create a class for each replacer
    replacers: dict[ str, # ACCENT-COLOR
        dict[ str, # default, light/dark
            str | dict[str, int] # random string, s/l/a
        ]
    ]
    # TODO: Create a class for each color
    colors: dict[str, dict[str, int]]

    def __init__(self, filename):
        colors_dict = json.load(open(filename))
        self.replacers = colors_dict["elements"]
        self.colors = colors_dict["colors"]
