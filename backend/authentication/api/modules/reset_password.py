import os
from django.db.models import Q
from dotenv import load_dotenv
from django.conf import settings
from django.db import IntegrityError
from authentication.models import MailToken
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import serializers, status, generics
from ..utils import create_uniform_response, OnlyUnAuthenticated

load_dotenv(settings.BASE_DIR / ".env")


class ResetPasswordSerializer(serializers.Serializer):
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
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        fields = None
        extra_kwargs = {
            "old_password": {"write_only": True},
            "new_password": {"write_only": True},
        }

    def validate_username_email(self, username, email):
        if email and username:
            user_obj = (
                self.context["view"]
                .get_queryset()
                .objects.filter(Q(username__iexact=username) & Q(email__iexact=email))
                .distinct()
            )

            if user_obj.exists():
                user_obj = user_obj.first()
                return user_obj
            else:
                return None
        else:
            raise serializers.ValidationError(
                {"Error": "Must include both username or email"}, code="natural"
            )

    @staticmethod
    def validate_mailtoken(user, token):
        try:
            token_database = MailToken.objects.get(user=user, token_type=3)
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

    def validate(self, value):
        token = value.get("token")
        email = value.get("email")
        username = value.get("username")
        new_password = value.get("new_password")

        instance = self.validate_username_email(username, email)
        if not instance:
            raise serializers.ValidationError(
                {"Error": "Invalid credentials"}, code="natural"
            )
        self.validate_mailtoken(instance, token)
        instance.set_password(new_password)
        instance.save()
        return value


class ResetPasswordView(generics.GenericAPIView):
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
    serializer_class = ResetPasswordSerializer
    permission_classes = [OnlyUnAuthenticated]

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        if self.serializer.is_valid():
            return Response(
                {
                    "code": "SUCCESS",
                    "message": "Password Updated Successfully",
                }
            )
        return Response(
            create_uniform_response(self.serializer.errors),
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )
