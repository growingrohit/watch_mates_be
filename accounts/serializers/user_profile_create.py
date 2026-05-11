from django.db import transaction
from rest_framework import serializers

from accounts.models import Profile, User


class UserProfileCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    display_name = serializers.CharField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    avatar = serializers.URLField(required=False, allow_blank=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "country_code",
            "mobile_number",
            "display_name",
            "bio",
            "avatar",
            "date_of_birth",
        )

    @transaction.atomic
    def create(self, validated_data):
        profile_payload = {
            "display_name": validated_data.pop("display_name", ""),
            "bio": validated_data.pop("bio", ""),
            "avatar": validated_data.pop("avatar", ""),
            "date_of_birth": validated_data.pop("date_of_birth", None),
        }
        password = validated_data.pop("password")

        user = User.objects.create_user(password=password, **validated_data)
        Profile.objects.create(user=user, **profile_payload)
        return user
