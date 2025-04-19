from scripts.utils.theme.theme import Theme


def define_arguments(parser):
    color_args = parser.add_argument_group('Color tweaks')
    color_args.add_argument('-O', '--opaque', action='store_true', help='make the background in menus/popovers opaque')


def apply_tweak(args, theme: Theme, colors):
    if args.opaque:
        with open(theme.main_styles, "r") as file:
            content = file.read()
        with open(theme.main_styles, "w") as file:
            replaced_content = content.replace("BACKGROUND-COLOR", "BACKGROUND-OPAQUE-COLOR")
            file.write(replaced_content)