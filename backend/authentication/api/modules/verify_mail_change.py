import os
from dotenv import load_dotenv
from django.conf import settings
from django.db import IntegrityError
from ..tasks import send_email_accept_mail
from ..utils import create_uniform_response
from authentication.models import MailToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, status, generics

load_dotenv(settings.BASE_DIR / ".env")


class VerifyMailChangeSerializer(serializers.Serializer):
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

    token = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    new_email = serializers.EmailField(required=True)
    old_email = serializers.EmailField(required=True)

    class Meta:
        fields = None

    def validate(self, value):
        token = value.get("token")
        username = value.get("username")
        new_email = value.get("new_email")
        old_email = value.get("old_email")

        user = self.context["request"].user
        if user.email != old_email:
            raise serializers.ValidationError(
                {"Error": "Wrong email provided"}, code="natural"
            )
        self.validate_mailtoken(user, token)
        user.email = new_email
        user.save()
        send_email_accept_mail(user.first_name, user.username, user.email)
        return user

    @staticmethod
    def validate_mailtoken(user, token):
        try:
            token_database = MailToken.objects.get(user=user, token_type=2)
            if token_database.key == token:
                token_database.delete()
                return token
            raise serializers.ValidationError(
                {"Error": "Expired Token"}, code="natural"
            )
        except MailToken.DoesNotExist:
            raise serializers.ValidationError(
                {"Error": "Invalid Token"}, code="natural"
            )


class VerifyMailChangeView(generics.GenericAPIView):
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

    serializer_class = VerifyMailChangeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        if self.serializer.is_valid():
            return Response(
                {"message": "Mail successfully updated <br> Logout and use new mail"}
            )
        return Response(
            create_uniform_response(self.serializer.errors),
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )
