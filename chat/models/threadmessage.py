from django.db import models

from common.abstract import AbstractCompleteAudit

from chat.models import Thread
from accounts.models import Profile

class ThreadMessage(AbstractCompleteAudit):
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
    )
    message = models.TextField()
    
    
    def __str__(self):
        return f"{self.thread} - {self.created_by}"