from django.db import models

from common.abstract import AbstractCompleteAudit

from accounts.models import Profile
from chat.models import Thread


class ThreadMember(AbstractCompleteAudit):
    member = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="thread_member",
    )
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = [["member", "thread"]]
        ordering = ["member"]


    def __str__(self):
        return f"{self.thread} - {self.member}"