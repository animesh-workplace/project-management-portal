import os
from django.db.models import Q
from dotenv import load_dotenv
from django.conf import settings
from django.db import IntegrityError
from user_management.models import MailToken
from rest_framework.response import Response
from ..tasks import send_email_reset_password
from django.contrib.auth import get_user_model
from rest_framework import serializers, status, generics
from ..utils import create_uniform_response, OnlyUnAuthenticated

load_dotenv(settings.BASE_DIR / ".env")


class ForgotPasswordSerializer(serializers.Serializer):
    """Cookie Refresh Serializer: Extracts the refresh cookie token from the user request

    Parameters
    ----------
    jwt-refresh : Cookie
            The cookie containing the refresh token

    Returns
    -------
    String
        Refresh token
    """

    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)

    class Meta:
        fields = None

    def validate_username_email(self, username, email):
        if email:
            user = self.authenticate(email=email)
        elif username:
            user = self.authenticate(username=username)
        else:
            raise serializers.ValidationError(
                {"Error": "Must include either username or email"}, code="natural"
            )
        return user

    def authenticate(self, username=None, email=None):
        user_obj = (
            self.context["view"]
            .get_queryset()
            .objects.filter(Q(username__iexact=username) | Q(email__iexact=email))
            .distinct()
        )

        if user_obj.exists():
            user_obj = user_obj.first()
            return user_obj
        return None

    def validate(self, value):
        email = value.get("email")
        username = value.get("username")
        instance = self.validate_username_email(username, email)
        if not instance:
            raise serializers.ValidationError(
                {"Error": "Invalid credentials"}, code="natural"
            )
        try:
            token = MailToken.objects.create(user=instance, token_type=3)
            link = (
                f"{os.getenv('BASE_LINK')}{os.getenv('BASE_URL')}auth/verify?username={instance.username}"
                f"&email={instance.email}&token={token}"
            )
            send_email_reset_password(
                instance.first_name, instance.username, instance.email, link
            )
            return value
        except IntegrityError:
            raise serializers.ValidationError(
                {"Error": "Mail already sent"}, code="natural"
            )


class ForgotPasswordView(generics.GenericAPIView):
    """Authentication Status API: Send the user authentication status

    Parameters
    ----------
    jwt-auth : Cookie
            The cookie containing the auth token
    jwt-refresh : Cookie
            The cookie containing the refresh token

    Returns
    -------
    String
        Authentication status:
            - Refreshable
            - Authenticated
            - Unauthenticated
    """

    queryset = get_user_model()
    serializer_class = ForgotPasswordSerializer
    permission_classes = [OnlyUnAuthenticated]

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        if self.serializer.is_valid():
            return Response(
                {
                    "code": "SUCCESS",
                    "message": "Please, verify in your mail",
                }
            )
        return Response(
            create_uniform_response(self.serializer.errors),
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )
