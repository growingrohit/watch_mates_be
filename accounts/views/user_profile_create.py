from rest_framework import generics, permissions, status
from rest_framework.response import Response

from accounts.serializers import UserProfileCreateSerializer


class UserProfileCreateAPIView(generics.CreateAPIView):
    serializer_class = UserProfileCreateSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "message": "User and profile created successfully.",
                "data": {
                    "id": str(user.id),
                    "username": user.username,
                    "email": user.email,
                    "full_name": user.full_name,
                },
            },
            status=status.HTTP_201_CREATED,
        )
