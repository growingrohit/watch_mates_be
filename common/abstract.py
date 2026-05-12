import uuid
from django.db import models

from watch_mates.settings import AUTH_USER_MODEL


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


class AbstractCreatedBy(models.Model):
    created_by = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_created_by",
    )

    class Meta:
        abstract = True


class AbstractUpdatedBy(models.Model):
    updated_by = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_updated_by",
    )

    class Meta:
        abstract = True