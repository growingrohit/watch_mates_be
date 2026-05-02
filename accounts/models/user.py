from django.contrib.auth.models import AbstractUser
from django.db import models

from common.abstract import AbstractAudit


class User(AbstractAudit, AbstractUser):
    username = models.CharField(max_length=128, unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    country_code = models.CharField(max_length=8, blank=True)
    mobile_number = models.CharField(max_length=10, unique=True, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["username"]),
            models.Index(fields=["full_name"]),
            models.Index(fields=["mobile_number"]),
        ]

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.full_name = f"{self.first_name} {self.last_name}".strip()
        super().save(*args, **kwargs)
