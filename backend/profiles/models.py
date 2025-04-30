from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile', primary_key=True
    )

    display_name = models.CharField(max_length=20, null=True, blank=True)

    image = models.ImageField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ('-created',)

    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
        pass

    @property
    def username(self):
        return self.user.username
