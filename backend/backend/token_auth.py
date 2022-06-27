from http import cookies
from django.db import close_old_connections
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from channels.exceptions import DenyConnection
from django.contrib.auth.models import AnonymousUser

# from rest_framework_simplejwt.tokens import AccessToken


@database_sync_to_async
def get_authenticated_user(scope):
    try:
        cookie = next(x for x in scope["headers"] if x[0].decode("utf-8") == "cookie")[
            1
        ].decode("utf-8")
        jwt_value = cookies.SimpleCookie(cookie)["c_uid"].value
        if jwt_value is None:
            return AnonymousUser()

        try:
            # payload = AccessToken(jwt_value)
            print(payload)
            # payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            msg = _("Signature has expired")
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = _("Error decoding signature")
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        User = get_user_model()
        # username = jwt_get_username_from_payload(payload)

        if not username:
            msg = _("Invalid payload")
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            msg = _("Invalid signature")
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = _("User account is disabled")
            raise exceptions.AuthenticationFailed(msg)

        return user
    except:
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    """
    Token authorization middleware for Django Channels 3
    """

    async def __call__(self, scope, receive, send):
        try:
            # Close old database connections to prevent usage of timed out connections
            close_old_connections()
            user = await get_authenticated_user(scope)
            scope["user"] = user
        except:
            DenyConnection()

        return await super().__call__(scope, receive, send)
