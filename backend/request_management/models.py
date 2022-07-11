from django.db import models
from user_management.models import User
from schema_management.models import ProjectHandler

# Create your models here.

STATUS_CHOICES = (
    ("1", "Requested"),
    ("2", "Accepted"),
    ("3", "Rejected"),
)


class UserRequest(models.Model):
    sop = models.TextField(default=False)
    comments = models.TextField(default=False)
    submitted_time = models.DateTimeField(auto_now=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    projects = models.OneToOneField(
        ProjectHandler, on_delete=models.CASCADE, primary_key=False
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="1")
    response_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
