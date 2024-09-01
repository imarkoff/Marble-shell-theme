from scripts import config
from scripts.utils import hex_to_rgba
panel_folder = f"{config.tweaks_folder}/panel"


def define_arguments(parser):
    panel_args = parser.add_argument_group('Panel tweaks')
    panel_args.add_argument('-Pds', '--panel_default_size', action='store_true', help='set default panel size')
    panel_args.add_argument('-Pnp', '--panel_no_pill', action='store_true', help='remove panel button background')
    panel_args.add_argument('-Ptc', '--panel_text_color', type=str, nargs='?', help='custom panel HEX(A) text color')


def apply_tweak(args, theme, colors):
    if args.panel_default_size:
        with open(f"{panel_folder}/def-size.css", "r") as f:
            theme += f.read()

    if args.panel_no_pill:
        with open(f"{panel_folder}/no-pill.css", "r") as f:
            theme += f.read()

    if args.panel_text_color:
        theme += ".panel-button,\
                    .clock,\
                    .clock-display StIcon {\
                        color: rgba(" + ', '.join(map(str, hex_to_rgba(args.panel_text_color))) + ");\
                    }"
