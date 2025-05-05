import os

from io import BytesIO

from PIL import Image

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files import File


class ImageSizeValidator:
    """
    A validator to ensure that the size of an uploaded image file does not exceed a specified maximum size.
    """

    def __init__(self, max_size_mb=None):
        self.max_size_mb = max_size_mb or getattr(settings, 'MAX_IMAGE_SIZE', 20)

    def __call__(self, file):
        max_size_bytes = self.max_size_mb * 1024 * 1024
        current_size_mb = file.size / (1024 * 1024)

        if file.size > max_size_bytes:
            raise ValidationError(
                f'Image size cannot exceed {self.max_size_mb:.2f} MB. Current file size: {current_size_mb:.2f} MB'
            )
        

def compress_image(file, quality=50):
    """
    Compresses an image file by converting it to JPEG format and reducing its quality.
    """

    try:
        image = Image.open(file)
        image_io = BytesIO()

        if image.mode in ('P', 'RGBA'):
            image = image.convert('RGB')
        
        image.save(image_io, format='JPEG', quality=quality, optimize=True)

        base_name = os.path.splitext(file.name)[0]
        new_name = f'{base_name}.jpg'

        image_io.seek(0)

        return File(image_io, name=new_name)
    except Exception as e:
        return file
