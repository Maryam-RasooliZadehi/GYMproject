from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.utils import timezone


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin panel for user management with add and change forms plus password
    """

    model = User
    list_display = ("phone_number","email", "is_superuser", "is_active","user_type")
    list_filter = ("is_superuser", "is_active")
    searching_fields = ("phone_number",)
    ordering = ("email",)
    readonly_fields =("last_login","created_date","updated_date")
    fieldsets = (
        (
            "Authentication",
            {
                "fields": ("phone_number", "password"),
            },
        ),
        (
            "permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                ),
            },
        ),
        (
            "group permissions",
            {
                "fields": ("groups", "user_permissions"),
            },
        ),
        (
            "important dates",
            {
                "fields": ("last_login","created_date","updated_date"),
            },
        ),
        (
            "other fields",
            {
                "fields": ("email","first_name","last_name","user_type"),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "password1",
                    "password2",
                    "is_active",
                    "user_type",
                    "is_superuser",
                ),
            },
        ),
    )