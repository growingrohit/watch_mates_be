from django.db import models

from common.abstract import AbstractCompleteAudit


class ThreadKind(models.TextChoices):
    DIRECT = "direct", "Direct"
    GROUP = "group", "Group"
    CHANNEL = "channel", "Channel"
    PRIVATE = "private", "Private"


class Thread(AbstractCompleteAudit):
    name = models.CharField(
        max_length=255, blank=True
    )
    profile_image = models.URLField(blank=True)
    kind = models.CharField(
        max_length=255,
        choices=ThreadKind.choices,
        default=ThreadKind.DIRECT,
    )
    last_message = models.ForeignKey(
        "chat.ThreadMessage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="thread_last_message",
    )

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.created_by}"

    
    def update_last_message(self):
        self.last_message = self.threadmessage_set.filter(
            is_active=True
        ).order_by("-created_at").first()

        self.save(update_fields=["last_message"])