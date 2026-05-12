from django.db import models

from common.abstract import AbstractCompleteAudit

class Thread(AbstractCompleteAudit):
    name = models.CharField(
        max_length=255, blank=True
    )
    profile_image = models.URLField(blank=True)
    is_group = models.BooleanField(
        default=False
    )

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.created_by}"