import os
import logging
import shortuuid

from django.db import models
from django.contrib.auth import get_user_model
from django.templatetags.static import static
from django.core.validators import FileExtensionValidator

from core.utils import ImageSizeValidator, compress_image


logger = logging.getLogger(__name__)


User = get_user_model()

ALLOWED_EXTENSIONS = ('jpg', 'jpeg', 'png', 'gif', 'webp')
DEFAULT_IMAGE_PATH = 'static/img/defaults/default.png'


def upload_to(instance, filename):
    ext = os.path.splitext(filename)[-1].lower()
    new_filename = shortuuid.uuid()[:8]

    return f'profiles/{str(instance.pk)[:8]}/{new_filename}{ext}'


class Profile(models.Model):
    """
    Profile model represents a user's profile in the application.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile', primary_key=True
    )

    display_name = models.CharField(max_length=20, null=True, blank=True)

    image = models.ImageField(
        upload_to=upload_to, null=True, blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS),
            ImageSizeValidator(),
        ]
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ('-created',)

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        is_new = self._state.adding

        if is_new and not self.display_name:
            self.display_name = self.user.username

        if self.image and self.pk:
            old_instance = Profile.objects.filter(pk=self.pk).first()

            if old_instance and old_instance.image and old_instance.image.name == self.image.name:
                super().save(*args, **kwargs)
                return
            
            try:
                self.image = compress_image(self.image)
            except Exception as e:
                logger.warning(f'Image compression failed for user {self.user}: {e}')
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        pass

    @property
    def username(self):
        return self.user.username
    
    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return static('img/defaults/default.png')
