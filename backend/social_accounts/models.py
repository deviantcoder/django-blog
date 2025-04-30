from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class SocialAccount(models.Model):
    PROVIDER_CHOICES = (
        ('google', 'Google'),
        ('github', 'GitHub'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_accounts')

    provider = models.CharField(max_length=10, choices=PROVIDER_CHOICES)
    uid = models.CharField(max_length=255, unique=True)

    extra_data = models.JSONField(default=dict, blank=True)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Social Account'
        verbose_name_plural = 'Social Accounts'
        unique_together = ('provider', 'uid')
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user.username}: {self.provider}'
