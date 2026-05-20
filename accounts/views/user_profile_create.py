from rest_framework import generics, permissions, status
from rest_framework.response import Response

from accounts.serializers import UserProfileCreateSerializer
from accounts.utils import build_auth_response_data


class UserProfileCreateAPIView(generics.CreateAPIView):
    serializer_class = UserProfileCreateSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            build_auth_response_data(
                "User and profile created successfully.",
                user,
            ),
            status=status.HTTP_201_CREATED,
        )
