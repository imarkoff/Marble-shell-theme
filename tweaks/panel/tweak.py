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
    panel_args.add_argument('--floating-panel', action='store_true', help='make the panel floating (transparent background)')


def apply_tweak(args, theme: Theme, colors):
    if args.panel_default_size:
        theme.add_from_file(f"{panel_folder}/def-size.css")

    if args.floating_panel:
        theme.add_from_file(f"{panel_folder}/floating-panel.css")
        if args.opaque:
            theme.add_from_file(f"{panel_folder}/floating-panel-opaque.css")

    if args.panel_no_pill:
        theme.add_from_file(f"{panel_folder}/no-pill.css")

    if args.wider_panel:
        theme.add_from_file(f"{panel_folder}/wider-panel.css")

    resolve_panel_text_color(theme, args.panel_text_color)

    if args.panel_grouped_buttons:
        theme.add_from_file(f"{panel_folder}/grouped-buttons.css")


def resolve_panel_text_color(theme: Theme, argument_property):
    if not argument_property: return

    (r, g, b, a) = ColorConverterImpl.hex_to_rgba(argument_property)
    final_color = f"rgba({r}, {g}, {b}, {a})"

    with open(f"{panel_folder}/text-color.css", "r") as file:
        content = file.read()

    replaced_content = content.replace("REPLACEMENT-COLOR", final_color)
    theme += replaced_content