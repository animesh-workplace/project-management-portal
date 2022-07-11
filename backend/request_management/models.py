from django.db import models
from schema_management.models import ProjectHandler
from user_management.models import User

# Create your models here.

STATUS_CHOICES = (
    ("1", "Requested"),
    ("2", "Accepted"),
    ("3", "Rejected"),
)


class UserRequest(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    requested_projects = models.OneToOneField(
        ProjectHandler, on_delete=models.CASCADE, primary_key=False
    )
    request_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="1")
    submitted_time = models.DateTimeField(auto_now=True)
    response_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    response_message = models.TextField(default=False)
    response_description = models.TextField(default=False)

    def __str__(self):
        return self.request_status
