from scripts import config
from scripts.utils.color_converter import ColorConverterImpl

panel_folder = f"{config.tweaks_folder}/panel"


def define_arguments(parser):
    panel_args = parser.add_argument_group('Panel tweaks')
    panel_args.add_argument('-Pds', '--panel-default-size', action='store_true', help='set default panel size')
    panel_args.add_argument('-Pnp', '--panel-no-pill', action='store_true', help='remove panel button background')
    panel_args.add_argument('-Ptc', '--panel-text-color', type=str, nargs='?', help='custom panel HEX(A) text color')
    panel_args.add_argument('--wider-panel', action='store_true', help='make the panel wider')


def apply_tweak(args, theme, colors):
    if args.panel_no_pill:
        with open(f"{panel_folder}/no-pill.css", "r") as f:
            theme += f.read()

    if args.panel_default_size:
        with open(f"{panel_folder}/def-size.css", "r") as f:
            theme += f.read()

    if args.wider_panel:
        with open(f"{panel_folder}/wider-panel.css", "r") as f:
            theme += f.read()

    if args.panel_text_color:
        theme += ".panel-button,\
                    .clock,\
                    .clock-display StIcon {\
                        color: rgba(" + ', '.join(map(str, ColorConverterImpl.hex_to_rgba(args.panel_text_color))) + ");\
                    }"
