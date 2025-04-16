from scripts import config
from scripts.utils.theme.theme import Theme

overview_folder = f"{config.tweaks_folder}/overview"


def define_arguments(parser):
    overview_args = parser.add_argument_group('Overview tweaks')
    overview_args.add_argument('--launchpad', action='store_true', help='change Show Apps icon to macOS Launchpad icon')


def apply_tweak(args, theme: Theme, colors):
    if args.launchpad:
        theme.add_from_file(f"{overview_folder}/launchpad/launchpad.css")
        theme *= f"{overview_folder}/launchpad/launchpad.png"
