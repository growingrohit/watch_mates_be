from django.db import models

from common.abstract import AbstractAudit
from accounts.models import Profile

class Thread(AbstractAudit):
    name = models.CharField(
        max_length=255, blank=True
    )
    created_by = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )
    is_group = models.BooleanField(
        default=False
    )

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["is_group"]),
        ]

    def __str__(self):
        return f"{self.name} - {self.created_by}"