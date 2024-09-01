from scripts import config
overview_folder = f"{config.tweaks_folder}/overview"


def define_arguments(parser):
    overview_args = parser.add_argument_group('Overview tweaks')
    overview_args.add_argument('--launchpad', action='store_true', help='change Show Apps icon to macOS Launchpad icon')


def apply_tweak(args, theme, colors):
    if args.launchpad:
        with open(f"{overview_folder}/launchpad/launchpad.css", "r") as f:
            theme += f.read()

        theme *= f"{overview_folder}/launchpad/launchpad.png"
