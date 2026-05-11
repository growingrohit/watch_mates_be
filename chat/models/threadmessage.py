from django.db import models

from common.abstract import AbstractAudit

from chat.models import Thread
from accounts.models import Profile

class ThreadMessage(AbstractAudit):
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
    )
    message = models.TextField()
    created_by = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )
    
    def __str__(self):
        return f"{self.thread} - {self.created_by}"