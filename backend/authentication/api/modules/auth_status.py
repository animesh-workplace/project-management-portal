from django.conf import settings
from ..utils import create_uniform_response
from rest_framework.response import Response
from rest_framework import serializers, status, generics


class CheckRefreshabilitySerializer(serializers.Serializer):
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

    def extract_refresh_token_status(self):
        request = self.context['request']
        cookie_name = getattr(settings, 'JWT_AUTH_REFRESH_COOKIE', None)
        if(cookie_name and cookie_name in request.COOKIES):
            return 'Refreshable'
        else:
            return 'Unauthenticated'

    def validate(self, value):
        return self.extract_refresh_token_status()


class AuthenticationStatusView(generics.GenericAPIView):
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
    serializer_class = CheckRefreshabilitySerializer
    permission_classes = []

    def get_authentication_status(self, auth_status):
        data = {
            'code': 'SUCCESS',
            'message': auth_status,
        }
        response = Response(data, status=status.HTTP_200_OK)
        return response

    def post(self, request, *args, **kwargs):
        self.request = request
        if(self.request.user.is_authenticated):
            return self.get_authentication_status('Authenticated')
        else:
            self.serializer = self.get_serializer(data=self.request.data)
            if(self.serializer.is_valid()):
                return self.get_authentication_status(self.serializer.validated_data)
        return Response(create_uniform_response(self.serializer.errors), status=status.HTTP_406_NOT_ACCEPTABLE)
