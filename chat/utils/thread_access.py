from django.db.models import Q, Prefetch
from django.shortcuts import get_object_or_404

from chat.models import Thread, ThreadMember


def threads_queryset_for_user(user):
    return (
        Thread.objects.filter(is_active=True)
        .filter(
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
    )


def get_thread_for_user(user, thread_id):
    return get_object_or_404(threads_queryset_for_user(user), pk=thread_id)
