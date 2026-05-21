from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Profile
from chat.models import Thread, ThreadMember
from chat.serializers import ThreadReadSerializer, ThreadWriteSerializer


class ThreadAPIView(APIView):
    """
    Generic thread endpoint:
    - GET /api/chat/threads/       → list
    - GET /api/chat/threads/<id>/  → retrieve
    - PUT /api/chat/threads/       → create
    - PUT /api/chat/threads/<id>/  → update
    """

    permission_classes = [IsAuthenticated]

    def _threads_for_user(self, user):
        return (
            Thread.objects.filter(is_active=True).filter(
                Q(created_by=user)
                | Q(
                    threadmember__member__user=user,
                    threadmember__is_active=True,
                )
            )
            .distinct()
            .prefetch_related(
                Prefetch(
                    "threadmember_set",
                    queryset=ThreadMember.objects.filter(is_active=True).select_related(
                        "member",
                        "member__user",
                    ),
                )
            )
            .select_related("created_by", "updated_by", "last_message")
            .order_by("-created_at")
        )

    def _get_thread(self, user, pk):
        return get_object_or_404(self._threads_for_user(user), pk=pk)

    def _response(self, message, data, status_code):
        return Response(
            {"message": message, "data": data},
            status=status_code,
        )

    def get(self, request, pk=None):
        if pk:
            thread = self._get_thread(request.user, pk)
            serializer = ThreadReadSerializer(thread)
            return self._response(
                "Thread retrieved successfully.",
                serializer.data,
                status.HTTP_200_OK,
            )

        threads = self._threads_for_user(request.user)
        serializer = ThreadReadSerializer(threads, many=True)
        return self._response(
            "Threads retrieved successfully.",
            serializer.data,
            status.HTTP_200_OK,
        )

    def put(self, request, pk=None):
        write_serializer = ThreadWriteSerializer(data=request.data)
        write_serializer.is_valid(raise_exception=True)

        if pk:
            thread = self._get_thread(request.user, pk)
            thread = write_serializer.update(
                thread,
                write_serializer.validated_data,
                request.user,
            )
            message = "Thread updated successfully."
            status_code = status.HTTP_200_OK
        else:
            thread = write_serializer.create(
                write_serializer.validated_data,
                request.user,
            )
            message = "Thread created successfully."
            status_code = status.HTTP_201_CREATED

        thread = self._get_thread(request.user, thread.pk)
        read_serializer = ThreadReadSerializer(thread)
        return self._response(message, read_serializer.data, status_code)
