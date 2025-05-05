import os
import shutil
import logging

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Profile


User = get_user_model()

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance
        )


@receiver(post_delete, sender=Profile)
def delete_profile_media_files(sender, instance, **kwargs):
    try:
        path = f'media/profiles/{str(instance.pk)[:8]}'
        if os.path.exists(path):
            shutil.rmtree(path)
    except Exception as e:
        logging.warning(f'Media deletion dailed for: {instance.user.username}', level='warning')
