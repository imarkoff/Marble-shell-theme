def define_arguments(parser):
    color_args = parser.add_argument_group('Color tweaks')
    color_args.add_argument('-O', '--opaque', action='store_true', help='make the background in menus/popovers opaque')


def apply_tweak(args, theme, colors):
    if args.opaque:
        colors["elements"]["BACKGROUND-COLOR"]["light"]["a"] = 1
        colors["elements"]["BACKGROUND-COLOR"]["dark"]["a"] = 1
