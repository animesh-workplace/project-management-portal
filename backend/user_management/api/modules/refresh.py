from django.conf import settings
from django.utils import timezone
from ..utils import create_uniform_response
from .jwt_utils import set_jwt_access_cookie
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


class CookieRefreshSerializer(TokenRefreshSerializer):
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

    refresh = serializers.CharField(required=False, help_text="Will override cookie")

    def extract_refresh_token(self):
        request = self.context["request"]
        cookie_name = getattr(settings, "JWT_AUTH_REFRESH_COOKIE", None)
        if cookie_name and cookie_name in request.COOKIES:
            return request.COOKIES.get(cookie_name)
        else:
            raise serializers.ValidationError(
                {"Error": "No valid refresh token found"}, code="natural"
            )

    def validate(self, value):
        refresh = RefreshToken(self.extract_refresh_token())
        return str(refresh.access_token)


class CookieRefreshView(TokenRefreshView):
    """Cookie Refresh API: Refreshes the cookie from the user's request

    Parameters
    ----------
    jwt-refresh : Cookie
            The cookie containing the refresh token

    Returns
    -------
    Cookie
        Refreshes jwt-auth token and updates the expiration date
    """

    serializer_class = CookieRefreshSerializer
    permission_classes = []

    def get_refreshed_token(self, access_token):
        data = {
            "code": "SUCCESS",
            "message": "Token Refreshed",
            "expiration": (
                timezone.localtime(timezone.now()) + settings.JWT_AUTH_LIFETIME
            ),
        }
        response = Response(data, status=status.HTTP_200_OK)
        set_jwt_access_cookie(response, access_token)
        return response

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        if self.serializer.is_valid():
            return self.get_refreshed_token(self.serializer.validated_data)
        return Response(
            create_uniform_response(self.serializer.errors),
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )
