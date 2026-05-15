from django.contrib import admin
from polymorphic.admin import (
    PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter,
    PolymorphicParentModelAdmin,
)

from chat.models import (
    Thread,
    ThreadMember, 
    ThreadMessage,
    TextMessage,
    MediaMessage,
    LinkMessage,
)

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by", "kind", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active", "kind")
    raw_id_fields = ("created_by", "updated_by")
    readonly_fields = ("created_at", "updated_at")
    save_as = True


@admin.register(ThreadMember)
class ThreadMemberAdmin(admin.ModelAdmin):
    list_display = ("thread", "member", "is_active")
    search_fields = ("member__display_name", "thread__name")
    list_filter = ("is_active",)
    raw_id_fields = ("thread", "member")
    readonly_fields = ("created_at", "updated_at")
    save_as = True


class ThreadMessageChildAdmin(PolymorphicChildModelAdmin):
    base_model = ThreadMessage
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = ("thread", "replied_to", "created_by", "updated_by")
    list_filter = ("is_active", "kind")
    ordering = ("-created_at",)


@admin.register(TextMessage)
class TextMessageAdmin(ThreadMessageChildAdmin):
    base_model = TextMessage
    list_display = ("thread", "created_by", "content", "kind", "created_at", "is_active")
    search_fields = ("content", "created_by__username", "thread__name")


@admin.register(MediaMessage)
class MediaMessageAdmin(ThreadMessageChildAdmin):
    base_model = MediaMessage
    list_display = (
        "thread",
        "created_by",
        "media_kind",
        "media_url",
        "kind",
        "created_at",
        "is_active",
    )
    search_fields = ("created_by__username", "thread__name")
    list_filter = ThreadMessageChildAdmin.list_filter + ("media_kind",)


@admin.register(LinkMessage)
class LinkMessageAdmin(ThreadMessageChildAdmin):
    base_model = LinkMessage
    list_display = (
        "thread",
        "created_by",
        "platform",
        "link",
        "kind",
        "created_at",
        "is_active",
    )
    search_fields = ("link", "created_by__username", "thread__name")
    list_filter = ThreadMessageChildAdmin.list_filter + ("platform",)


@admin.register(ThreadMessage)
class ThreadMessageAdmin(PolymorphicParentModelAdmin):
    base_model = ThreadMessage
    child_models = (TextMessage, MediaMessage, LinkMessage)
    list_display = (
        "thread",
        "message_type",
        "message_preview",
        "created_by",
        "kind",
        "delivered_time",
        "created_at",
        "is_active",
    )
    list_filter = (PolymorphicChildModelFilter, "is_active", "kind")
    search_fields = ("created_by__username", "thread__name")
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = ("thread", "replied_to", "created_by", "updated_by")
    ordering = ("-created_at",)

    @admin.display(description="Type")
    def message_type(self, obj):
        return obj.get_real_instance_class().__name__

    @admin.display(description="Preview")
    def message_preview(self, obj):
        instance = obj.get_real_instance()
        if isinstance(instance, TextMessage):
            return instance.content[:80]
        if isinstance(instance, MediaMessage):
            return instance.media_url
        if isinstance(instance, LinkMessage):
            return instance.link
        return "—"
