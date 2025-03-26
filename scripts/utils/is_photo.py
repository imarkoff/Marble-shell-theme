image_extensions = [
        'jpg', 'jpeg', 'png', 'gif', 'bmp',
        'webp', 'tiff', 'tif', 'svg', 'heic', 'heif'
    ]

def is_photo(extension: str):
    """
    Check if extension is supported photo format
    """

    return extension.lower() in image_extensions

class NotSupportedPhotoExtension(Exception):
    """
    Exception for not supported photo extension
    """

    def __init__(self, extension):
        self.message = (f"Photo extension {extension} is not supported. "
                        f"Supported formats: {', '.join(image_extensions)}.")
        super().__init__(self.message)