from django.db import models

from common.abstract import AbstractAudit

from accounts.models import Profile
from chat.models import Thread


class ThreadMember(AbstractAudit):
    member = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = [["member", "thread"]]


    def __str__(self):
        return f"{self.thread} - {self.member}"