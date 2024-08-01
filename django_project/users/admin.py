from django.contrib import admin

from .models import BaseUser

@admin.register(BaseUser)
class BaseUserAdmin(admin.ModelAdmin):
    list_display = ("username", "is_active",)
    list_filter = ("email", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions",
         {"fields":
              ( "is_active",
                "groups",
                "user_permissions",
                'phone',
                'level_user',
            )
        }),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
