import os.path
import shutil
import subprocess
from argparse import ArgumentParser
from scripts import config
from scripts.utils.is_photo import is_photo, NotSupportedPhotoExtension

def define_arguments(parser: ArgumentParser):
    gdm_args = parser.add_argument_group("GDM tweaks")
    gdm_args.add_argument("--gdm-image", type=str, nargs="?", help="Set GDM background image")
    gdm_args.add_argument("--gdm-blur", type=int, nargs="?", help="Blur GDM background image (px)")
    gdm_args.add_argument("--gdm-darken", type=int, choices=range(0, 100), help="Darken GDM background image (%%)", metavar="(0 - 100)")
    gdm_args.add_argument("--gdm-lighten",  type=int, choices=range(0, 100), help="Lighten GDM background image", metavar="(0 - 100)")


def apply_tweak(args, theme, colors):
    if args.gdm_image:
        gdm_image = GDMImage(args.gdm_image, config.temp_folder, args.gdm_blur)

        destination_dir = os.path.join(config.temp_folder, config.gdm_folder, config.raw_theme_folder)
        os.makedirs(destination_dir, exist_ok=True)

        gdm_image.copy_image(destination_dir)

        theme += f"""
            .login-dialog {{
                background-image: url("{gdm_image.image_name}");
                background-size: cover;
                {f"box-shadow: inset 0 0 0 9999px rgba(0, 0, 0, {args.gdm_darken/100});" if args.gdm_darken else ""}
                {f"box-shadow: inset 0 0 0 9999px rgba(255, 255, 255, {args.gdm_lighten/100});" if args.gdm_lighten else ""}
            }}
        """


class GDMImage:
    """
    Class to apply effects to GDM background image
    """

    image_name: str

    def __init__(self, path: str, temp_folder: str, blur: int = None):
        self.path = path

        extension = path.split(".")[-1]
        if not is_photo(extension):
            raise NotSupportedPhotoExtension(extension)

        self.image_name = f"gdm-image.{extension}"
        self.destination_dir = temp_folder
        self.destination_file = os.path.join(self.destination_dir, self.image_name)

        if not os.path.exists(self.destination_file):
            self._create_file()
            self._magick_tweaks(blur)

    def copy_image(self, destination: str):
        dest_path = os.path.join(destination, self.image_name)
        shutil.copyfile(self.destination_file, dest_path)

    def _create_file(self):
        os.makedirs(self.destination_dir, exist_ok=True)
        shutil.copyfile(self.path, self.destination_file)

    def _magick_tweaks(self, blur: int = None):
        if not shutil.which("magick"):
            print("Warning: ImageMagick not found. Image effects will be skipped.")
            return

        file = self.destination_file

        modified = False
        command = ["magick", file]

        if blur:
            command.extend(["-blur", f"0x{blur}"])
            modified = True

        if modified:
            print("Applying image filters... This may take a while.")
            output_file = file
            command.append(output_file)
            try:
                subprocess.run(command, check=True)
            except subprocess.CalledProcessError:
                print(f"Error: Failed to apply image effects to {file}")