from django.contrib import admin
from .models import User, MailToken
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "user_type",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            "Additional Fields",
            {
                "fields": (
                    "user_type",
                    "login_history",
                    "avatar",
                    "birth_date",
                    "address",
                    "city",
                    "state",
                    "pin_code",
                    "institute",
                    "job_profile",
                    "bio",
                ),
            },
        ),
    )


class MailTokenAdmin(admin.ModelAdmin):
    list_display = ("key", "user", "created", "token_type")
    fields = ("user", "token_type")
    ordering = ("-created",)


admin.site.register(User, AccountAdmin)
admin.site.register(MailToken, MailTokenAdmin)
