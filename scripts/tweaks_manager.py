import glob
import os
from scripts import config
import importlib.util


class TweaksManager:
    """
    Tweak manager class to load and apply tweaks from the tweak files in the tweaks folder
    (I think this class manages the tweaks)
    """

    def __init__(self):
        self.tweak_files = glob.glob(config.tweak_file)

    @staticmethod
    def load_tweak(tweak_file):
        """
        Load the tweak module        :return:
        """

        is_executable = os.access(tweak_file, os.X_OK)
        if not is_executable:
            os.chmod(tweak_file, 0o755)

        if os.access(tweak_file, os.X_OK):
            spec = importlib.util.spec_from_file_location("tweak_module", tweak_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module

        return None

    def define_arguments(self, parser):
        """
        Define arguments for the tweaks
        :param parser: ArgumentParser object
        """

        for tweak_file in self.tweak_files:
            tweak_module = self.load_tweak(tweak_file)

            if tweak_module:
                tweak_module.define_arguments(parser)

    def apply_tweaks(self, args, theme, colors):
        """
        Apply the tweaks
        :param args: parsed arguments
        :param theme: Theme object
        :param colors: colors.json object
        """

        for tweak_file in self.tweak_files:
            tweak_module = self.load_tweak(tweak_file)

            if tweak_module:
                tweak_module.apply_tweak(args, theme, colors)
