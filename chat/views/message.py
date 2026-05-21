from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from chat.models import ThreadMessage
from chat.serializers.message import MessageReadSerializer, MessageWriteSerializer
from chat.utils import get_thread_for_user


class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class ThreadMessageAPIView(APIView):
    """
    GET  /api/chat/threads/<thread_id>/messages/       — paginated list (newest first)
    PUT  /api/chat/threads/<thread_id>/messages/       — create
    PUT  /api/chat/threads/<thread_id>/messages/<pk>/  — update
    """

    permission_classes = [IsAuthenticated]
    pagination_class = MessagePagination

    def _response(self, message, data, status_code):
        return Response(
            {"message": message, "data": data},
            status=status_code,
        )

    def _get_message(self, thread, message_id, user):
        message = get_object_or_404(
            ThreadMessage.objects.filter(thread=thread),
            pk=message_id,
        )
        if message.created_by_id != user.id:
            raise PermissionDenied("You can only update your own messages.")
        return message

    def get(self, request, thread_id, pk=None):
        if pk:
            raise MethodNotAllowed("GET")

        thread = get_thread_for_user(request.user, thread_id)
        queryset = (
            ThreadMessage.objects.filter(thread=thread, is_active=True)
            .select_related("created_by", "updated_by", "replied_to")
            .order_by("-created_at")
        )

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)
        serializer = MessageReadSerializer(page, many=True)

        return Response(
            {
                "message": "Messages retrieved successfully.",
                "data": {
                    "count": paginator.page.paginator.count,
                    "next": paginator.get_next_link(),
                    "previous": paginator.get_previous_link(),
                    "results": serializer.data,
                },
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, thread_id, pk=None):
        thread = get_thread_for_user(request.user, thread_id)

        if pk:
            instance = self._get_message(thread, pk, request.user)
            write_serializer = MessageWriteSerializer(
                instance,
                data=request.data,
                partial=True,
                context={"thread": thread},
            )
        else:
            write_serializer = MessageWriteSerializer(
                data=request.data,
                context={"thread": thread},
            )

        write_serializer.is_valid(raise_exception=True)

        if pk:
            message = write_serializer.update(
                instance,
                write_serializer.validated_data,
                request.user,
            )
            response_message = "Message updated successfully."
            status_code = status.HTTP_200_OK
        else:
            message = write_serializer.create(
                write_serializer.validated_data,
                thread,
                request.user,
            )
            response_message = "Message created successfully."
            status_code = status.HTTP_201_CREATED

        read_serializer = MessageReadSerializer(message)
        return self._response(response_message, read_serializer.data, status_code)
