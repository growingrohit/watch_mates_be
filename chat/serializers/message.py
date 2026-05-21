from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from chat.models import (
    LinkMessage,
    MediaKind,
    MediaMessage,
    MessageKind,
    PlatformKind,
    TextMessage,
    ThreadMessage,
)


class MessageReadSerializer(serializers.Serializer):
    def to_representation(self, instance):
        message = instance.get_real_instance()
        data = {
            "id": str(message.id),
            "thread": str(message.thread_id),
            "kind": message.kind,
            "message_type": message.__class__.__name__,
            "delivered_time": message.delivered_time,
            "replied_to": str(message.replied_to_id) if message.replied_to_id else None,
            "is_active": message.is_active,
            "created_by": str(message.created_by_id),
            "created_by_username": message.created_by.username,
            "updated_by": str(message.updated_by_id),
            "created_at": message.created_at,
            "updated_at": message.updated_at,
        }

        if isinstance(message, TextMessage):
            data["content"] = message.content
        elif isinstance(message, MediaMessage):
            data["media_url"] = message.media_url
            data["media_kind"] = message.media_kind
        elif isinstance(message, LinkMessage):
            data["link"] = message.link
            data["platform"] = message.platform

        return data


class MessageWriteSerializer(serializers.Serializer):
    kind = serializers.ChoiceField(choices=MessageKind.choices)
    delivered_time = serializers.DateTimeField(required=False, allow_null=True)
    replied_to = serializers.UUIDField(required=False, allow_null=True)
    content = serializers.CharField(required=False, allow_blank=True)
    media_url = serializers.URLField(required=False, allow_blank=True)
    media_kind = serializers.ChoiceField(
        choices=MediaKind.choices,
        required=False,
    )
    link = serializers.URLField(required=False, allow_blank=True)
    platform = serializers.ChoiceField(
        choices=PlatformKind.choices,
        required=False,
    )

    def validate_replied_to(self, value):
        if value is None:
            return value
        thread = self.context["thread"]
        if not ThreadMessage.objects.filter(id=value, thread=thread).exists():
            raise serializers.ValidationError(
                "Replied-to message must belong to this thread."
            )
        return value

    def validate(self, attrs):
        kind = attrs.get("kind")
        if self.partial:
            return attrs

        if kind == MessageKind.TEXT and not attrs.get("content"):
            raise serializers.ValidationError(
                {"content": "Content is required for text messages."}
            )
        if kind == MessageKind.MEDIA and not attrs.get("media_url"):
            raise serializers.ValidationError(
                {"media_url": "Media URL is required for media messages."}
            )
        if kind == MessageKind.LINK and not attrs.get("link"):
            raise serializers.ValidationError(
                {"link": "Link is required for link messages."}
            )
        return attrs

    @transaction.atomic
    def create(self, validated_data, thread, user):
        kind = validated_data.pop("kind")
        replied_to_id = validated_data.pop("replied_to", None)
        delivered_time = validated_data.pop("delivered_time", None)

        common = {
            "thread": thread,
            "kind": kind,
            "created_by": user,
            "updated_by": user,
            "replied_to_id": replied_to_id,
            "delivered_time": delivered_time or timezone.now(),
        }

        if kind == MessageKind.TEXT:
            message = TextMessage.objects.create(
                content=validated_data.pop("content"),
                **common,
            )
        elif kind == MessageKind.MEDIA:
            message = MediaMessage.objects.create(
                media_url=validated_data.pop("media_url"),
                media_kind=validated_data.pop("media_kind", MediaKind.IMAGE),
                **common,
            )
        else:
            message = LinkMessage.objects.create(
                link=validated_data.pop("link"),
                platform=validated_data.pop("platform", PlatformKind.WEB),
                **common,
            )

        thread.update_last_message()

        return message

    @transaction.atomic
    def update(self, instance, validated_data, user):
        message = instance.get_real_instance()

        if "delivered_time" in validated_data:
            message.delivered_time = validated_data["delivered_time"]
        if "replied_to" in validated_data:
            message.replied_to_id = validated_data["replied_to"]
        if "is_active" in validated_data:
            message.is_active = validated_data["is_active"]

        if isinstance(message, TextMessage) and "content" in validated_data:
            message.content = validated_data["content"]
        if isinstance(message, MediaMessage):
            if "media_url" in validated_data:
                message.media_url = validated_data["media_url"]
            if "media_kind" in validated_data:
                message.media_kind = validated_data["media_kind"]
        if isinstance(message, LinkMessage):
            if "link" in validated_data:
                message.link = validated_data["link"]
            if "platform" in validated_data:
                message.platform = validated_data["platform"]

        message.updated_by = user
        message.save()
        return message
