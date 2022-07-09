from django.db import models
from django.conf import settings
from .storage import OverwriteStorage
from multiselectfield import MultiSelectField
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser
from schema_management.models import ProjectHandler

# Create your functions here
def upload_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f"user_{instance.id}_{instance}/images/{filename}"


PROJECT_CHOICES = tuple(ProjectHandler.objects.values_list("name", "name"))

# Create your models here
class User(AbstractUser):
    USER_TYPE = (
        (1, "Super Admin"),
        (2, "Project Admin"),
        (3, "General"),
    )
    bio = models.TextField(blank=True)
    login_history = models.JSONField(default=list)
    city = models.CharField(blank=True, max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    state = models.CharField(blank=True, max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    address = models.CharField(blank=True, max_length=1000)
    institute = models.CharField(blank=True, max_length=500)
    job_profile = models.CharField(blank=True, max_length=255)
    pin_code = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=0
    )
    user_type = models.DecimalField(
        default=3, max_digits=1, decimal_places=0, choices=USER_TYPE
    )
    avatar = models.ImageField(
        null=True,
        blank=True,
        storage=OverwriteStorage(),
        upload_to=upload_path,
        default="default/avatar.png",
    )
    projects = MultiSelectField(null=True, blank=True, choices=PROJECT_CHOICES)


class MailToken(Token):
    class Meta:
        verbose_name = "Mail Token"
        verbose_name_plural = "Mail Tokens"
        constraints = [
            models.UniqueConstraint(fields=["user", "token_type"], name="unique_key")
        ]

    TOKEN_TYPE = (
        (1, "Activation"),
        (2, "Mail change"),
        (3, "Forgot Password"),
        (4, "Upgrade"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="auth_token", on_delete=models.CASCADE
    )
    token_type = models.DecimalField(max_digits=1, decimal_places=0, choices=TOKEN_TYPE)
