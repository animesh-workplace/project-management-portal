from django.conf import settings
from rest_framework import status
from .jwt_utils import unset_jwt_cookies
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class LogoutView(APIView):
    """Logout API: Deletes the Token object assigned to the current User

    Parameters
    ----------
    jwt-auth : Cookie
            Cookie received after authenticating and used to get authenticated pages and data
    jwt-refresh : Cookie
            Cookie received after authenticating and used to get new auth token
    csrf_token : Cookie
            Cookie used to verify the Request source is same

    Returns
    -------
    Cookies
        Empties the cookies jwt-auth, jwt-refresh and csrf_token
    """
    permission_classes = []

    def post(self, request, *args, **kwargs):
        return self.logout(request)

    def logout(self, request):
        response = Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
        cookie_name = getattr(settings, 'JWT_AUTH_COOKIE', None)
        unset_jwt_cookies(response)
        return response
