from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from accounts.models import Profile, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = (
        "username",
        "full_name",
        "mobile_number",
        "is_active",
        "is_staff",
    )
    search_fields = ("username", "email", "full_name", "mobile_number")
    list_filter = ("is_active", "is_staff", "is_superuser")
    readonly_fields = ("created_at", "updated_at", "full_name")
    save_as = True
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "full_name",
                    "email",
                    "country_code",
                    "mobile_number",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "country_code",
                    "mobile_number",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "display_name", "date_of_birth", "is_active")
    search_fields = ("user__username", "display_name")
    list_filter = ("is_active",)
    raw_id_field = ("user",)
    readonly_fields = ("created_at", "updated_at")
    save_as = True