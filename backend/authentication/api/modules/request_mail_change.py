import os
from dotenv import load_dotenv
from django.conf import settings
from django.db import IntegrityError
from ..utils import create_uniform_response
from authentication.models import MailToken
from rest_framework.response import Response
from ..tasks import send_email_mail_change_request
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, status, generics

load_dotenv(settings.BASE_DIR / ".env")


class RequestMailChangeSerializer(serializers.Serializer):
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

    old_email = serializers.EmailField(required=True)
    new_email = serializers.EmailField(required=True)

    class Meta:
        fields = None

    def validate(self, value):
        new_email = value.get("new_email")
        old_email = value.get("old_email")
        if old_email == new_email:
            raise serializers.ValidationError(
                {"Error": "Both mail are identical"}, code="natural"
            )
        instance = self.context["request"].user
        if instance.email == old_email:
            try:
                token = MailToken.objects.create(user=instance, token_type=2)
                link = (
                    f"{os.getenv('BASE_LINK')}{os.getenv('BASE_URL')}activate?username={instance.username}"
                    f"&old_email={instance.email}&new_email={new_email}&token={token}"
                )
                send_email_mail_change_request(
                    instance.first_name, instance.username, old_email, new_email, link
                )
                return value
            except IntegrityError:
                raise serializers.ValidationError(
                    {"Error": "Mail already sent"}, code="natural"
                )
        raise serializers.ValidationError(
            {"Error": "Wrong email provided"}, code="natural"
        )


class RequestMailChangeView(generics.GenericAPIView):
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

    serializer_class = RequestMailChangeSerializer
    permission_classes = [IsAuthenticated]

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
