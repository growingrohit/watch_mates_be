from django.db import models
from polymorphic.models import PolymorphicModel

from common.abstract import AbstractCompleteAudit

from chat.models import Thread


class MessageKind(models.TextChoices):
    TEXT = "text", "Text"
    LINK = "link", "Link"
    MEDIA = "media", "Media"


class MediaKind(models.TextChoices):
    IMAGE = "image", "Image"
    AUDIO = "audio", "Audio"
    VIDEO = "video", "Video"


class PlatformKind(models.TextChoices):
    YOUTUBE = "youtube", "Youtube"
    INSTAGRAM = "instagram", "Instagram"
    FACEBOOK = "facebook", "Facebook"
    LINKEDIN = "linkedin", "LinkedIn"
    WEB = "web", "Web"


class ThreadMessage(PolymorphicModel, AbstractCompleteAudit):
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
    )
    delivered_time = models.DateTimeField(
        null=True
    )
    kind = models.CharField(
        max_length=255,
        choices=MessageKind.choices,
        default=MessageKind.TEXT,
    )

    replied_to = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True
    )
    
    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["thread"]),
        ]

    
    def __str__(self):
        return f"{self.thread} - {self.created_by}"


class TextMessage(ThreadMessage):
    content = models.TextField()

    class Meta:
        ordering = ["-created_at"]


class MediaMessage(ThreadMessage):
    media_url = models.URLField()
    kind = models.CharField(
        max_length=255,
        choices=MediaKind.choices,
        default=MediaKind.IMAGE,
    )

    class Meta:
        ordering = ["-created_at"]


class LinkMessage(ThreadMessage):
    link = models.URLField()
    platform = models.CharField(
        max_length=255,
        choices=PlatformKind.choices,
        default=PlatformKind.WEB,
    )

    class Meta:
        ordering = ["-created_at"]
