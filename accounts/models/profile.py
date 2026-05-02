from django.conf import settings
from django.db import models

from common.abstract import AbstractAudit


class Profile(AbstractAudit):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    display_name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.URLField(blank=True)
    profile_image = models.URLField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["date_of_birth"]),
        ]

    def __str__(self):
        return f"{self.display_name} - {self.user.username}"

