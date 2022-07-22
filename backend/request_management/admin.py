from .models import UserRequest
from django.contrib import admin

# Register your models here.
class UserReuestAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "status",
        "submitted_time",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "projects",
                    "response_time",
                    "status",
                    "sop",
                    "comments",
                )
            },
        ),
    )


admin.site.register(UserRequest, UserReuestAdmin)
