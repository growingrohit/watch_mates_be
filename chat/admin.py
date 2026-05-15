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

