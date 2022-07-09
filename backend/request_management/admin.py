from django.contrib import admin
from .models import UserRequest

# Register your models here.
class UserReuestAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "request_status",
        "submitted_time",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "requested_projects",
                    "response_time",
                    "request_status",
                    "response_message",
                    "response_description",
                )
            },
        ),
    )


admin.site.register(UserRequest, UserReuestAdmin)
