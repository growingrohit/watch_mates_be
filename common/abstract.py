import uuid
from django.db import models


class AbstractTimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractUUID(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class AbstractIsActive(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class AbstractAudit(AbstractUUID, AbstractTimeStamp, AbstractIsActive):
    
    class Meta:
        abstract = True