from django.db import models

from common.abstract import AbstractCompleteAudit

from chat.models import ThreadMessage
from accounts.models import Profile


class MessageReceipt(AbstractCompleteAudit):
    message = models.ForeignKey(
        ThreadMessage,
        on_delete=models.CASCADE,
    )
    receiver = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )
    received_datetime = models.DateTimeField(
        null=True
    )
    seen_datetime = models.DateTimeField(
        null=True
    )
    reaction = models.CharField(
        max_length=8, blank=True
    )

    class Meta:
        unique_together = [["message", "receiver"]]
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["message"]),
        ]

    def __str__(self):
        return f"{self.message} - {self.receiver}"

