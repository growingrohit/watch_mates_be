from django.db import transaction
from rest_framework import serializers

from accounts.models import Profile
from chat.models import Thread, ThreadKind, ThreadMember


class ThreadMemberReadSerializer(serializers.ModelSerializer):
    member_id = serializers.UUIDField(source="member.id", read_only=True)
    display_name = serializers.CharField(source="member.display_name", read_only=True)
    username = serializers.CharField(source="member.user.username", read_only=True)

    class Meta:
        model = ThreadMember
        fields = (
            "id",
            "member_id",
            "display_name",
            "username",
            "is_active",
            "created_at",
        )


class ThreadReadSerializer(serializers.ModelSerializer):
    members = ThreadMemberReadSerializer(
        source="threadmember_set",
        many=True,
        read_only=True,
    )
    created_by_username = serializers.CharField(
        source="created_by.username",
        read_only=True,
    )

    class Meta:
        model = Thread
        fields = (
            "id",
            "name",
            "profile_image",
            "kind",
            "is_active",
            "last_message",
            "created_by",
            "created_by_username",
            "updated_by",
            "created_at",
            "updated_at",
            "members",
        )
        read_only_fields = fields


class ThreadWriteSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    profile_image = serializers.URLField(required=False, allow_blank=True)
    kind = serializers.ChoiceField(choices=ThreadKind.choices, required=False)
    is_active = serializers.BooleanField(required=False)
    members = serializers.ListField(
        child=serializers.UUIDField(),
        required=False,
        allow_empty=True,
        help_text="List of profile IDs to add as thread members.",
    )

    def validate_members(self, value):
        if not value:
            return value

        existing = Profile.objects.filter(id__in=value).count()
        if existing != len(set(value)):
            raise serializers.ValidationError(
                "One or more profile IDs are invalid."
            )
        return list(set(value))

    @transaction.atomic
    def create(self, validated_data, user):
        member_ids = validated_data.pop("members", [])
        validated_data.setdefault("kind", ThreadKind.DIRECT)
        thread = Thread.objects.create(
            created_by=user,
            updated_by=user,
            **validated_data,
        )
        self._sync_members(thread, member_ids, user)
        return thread

    @transaction.atomic
    def update(self, instance, validated_data, user):
        member_ids = validated_data.pop("members", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.updated_by = user
        instance.save()

        if member_ids is not None:
            self._sync_members(instance, member_ids, user)

        return instance

    def _sync_members(self, thread, member_profile_ids, user):
        profile = Profile.objects.filter(user=user).first()
        if profile and profile.id not in member_profile_ids:
            member_profile_ids = [*member_profile_ids, profile.id]

        existing_members = ThreadMember.objects.filter(thread=thread)
        existing_ids = set(existing_members.values_list("member_id", flat=True))
        target_ids = set(member_profile_ids)

        remove_ids = existing_ids - target_ids
        add_ids = target_ids - existing_ids

        if remove_ids:
            existing_members.filter(member_id__in=remove_ids).update(
                is_active=False,
                updated_by=user,
            )

        for profile_id in add_ids:
            membership, created = ThreadMember.objects.get_or_create(
                thread=thread,
                member_id=profile_id,
                defaults={
                    "created_by": user,
                    "updated_by": user,
                    "is_active": True,
                },
            )
            if not created and not membership.is_active:
                membership.is_active = True
                membership.updated_by = user
                membership.save(update_fields=["is_active", "updated_by"])
