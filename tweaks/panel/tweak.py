from scripts import config
from scripts.utils.color_converter.color_converter_impl import ColorConverterImpl
from scripts.utils.theme.theme import Theme

panel_folder = f"{config.tweaks_folder}/panel"


def define_arguments(parser):
    panel_args = parser.add_argument_group('Panel tweaks')
    panel_args.add_argument('-Pds', '--panel-default-size', action='store_true', help='set default panel size')
    panel_args.add_argument('-Pnp', '--panel-no-pill', action='store_true', help='remove panel button background')
    panel_args.add_argument('-Ptc', '--panel-text-color', type=str, nargs='?', help='custom panel HEX(A) text color')
    panel_args.add_argument('--wider-panel', action='store_true', help='make the panel wider')
    panel_args.add_argument('--panel-grouped-buttons', action='store_true', help='group panel buttons together')


def apply_tweak(args, theme: Theme, colors):
    if args.panel_default_size:
        theme.add_from_file(f"{panel_folder}/def-size.css")

    if args.panel_no_pill:
        theme.add_from_file(f"{panel_folder}/no-pill.css")

    if args.wider_panel:
        theme.add_from_file(f"{panel_folder}/wider-panel.css")

    if args.panel_text_color:
        theme += ".panel-button,\
                    .clock,\
                    .clock-display StIcon {\
                        color: rgba(" + ', '.join(map(str, ColorConverterImpl.hex_to_rgba(args.panel_text_color))) + ");\
                    }"

    if args.panel_grouped_buttons:
        theme.add_from_file(f"{panel_folder}/grouped-buttons.css")