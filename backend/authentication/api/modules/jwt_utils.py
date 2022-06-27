from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from ..utils import import_callable
from django.middleware.csrf import _get_new_csrf_token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


def set_jwt_access_cookie(response, access_token):
    cookie_name = getattr(settings, 'JWT_AUTH_COOKIE', None)
    cookie_secure = getattr(settings, 'JWT_AUTH_SECURE', False)
    cookie_path = getattr(settings, 'JWT_AUTH_COOKIE_PATH', '/')
    cookie_httponly = getattr(settings, 'JWT_AUTH_HTTPONLY', True)
    cookie_samesite = getattr(settings, 'JWT_AUTH_SAMESITE', 'Lax')
    access_token_expiration = timezone.localtime(timezone.now()) + settings.JWT_AUTH_LIFETIME

    if(cookie_name):
        response.set_cookie(
            key=cookie_name,
            path=cookie_path,
            value=access_token,
            secure=cookie_secure,
            httponly=cookie_httponly,
            samesite=cookie_samesite,
            expires=access_token_expiration,
        )


def set_jwt_refresh_cookie(response, refresh_token):
    cookie_secure = getattr(settings, 'JWT_AUTH_SECURE', False)
    cookie_httponly = getattr(settings, 'JWT_AUTH_HTTPONLY', True)
    cookie_samesite = getattr(settings, 'JWT_AUTH_SAMESITE', 'Lax')
    refresh_cookie_name = getattr(settings, 'JWT_AUTH_REFRESH_COOKIE', None)
    refresh_cookie_path = getattr(settings, 'JWT_AUTH_REFRESH_COOKIE_PATH', '/')
    refresh_token_expiration = timezone.localtime(timezone.now()) + settings.JWT_AUTH_REFRESH_LIFETIME

    if(refresh_cookie_name):
        response.set_cookie(
            value=refresh_token,
            secure=cookie_secure,
            key=refresh_cookie_name,
            path=refresh_cookie_path,
            samesite=cookie_samesite,
            httponly=cookie_httponly,
            expires=refresh_token_expiration,
        )


def set_csrf_cookie(response, csrf_token):
    csrf_token_expiration = settings.CSRF_COOKIE_AGE
    csrf_cookie_path = getattr(settings, 'CSRF_COOKIE_PATH', '/')
    csrf_cookie_name = getattr(settings, 'CSRF_COOKIE_NAME', None)
    cookie_secure = getattr(settings, 'CSRF_COOKIE_SECURE', False)
    cookie_httponly = getattr(settings, 'CSRF_COOKIE_HTTPONLY', True)
    cookie_samesite = getattr(settings, 'CSRF_COOKIE_SAMESITE', 'Lax')

    response.set_cookie(
        value=csrf_token,
        key=csrf_cookie_name,
        secure=cookie_secure,
        path=csrf_cookie_path,
        samesite=cookie_samesite,
        httponly=cookie_httponly,
        expires=csrf_token_expiration,
    )


def set_jwt_cookies(response, access_token, refresh_token, csrf_token):
    set_jwt_access_cookie(response, access_token)
    set_jwt_refresh_cookie(response, refresh_token)
    set_csrf_cookie(response, csrf_token)


def jwt_encode(user):
    TOPS = import_callable(TokenObtainPairSerializer)
    refresh = TOPS.get_token(user)
    csrf_token = _get_new_csrf_token()
    return refresh.access_token, refresh, csrf_token


def unset_jwt_cookies(response):
    auth_cookie_name = getattr(settings, 'JWT_AUTH_COOKIE', None)
    csrf_cookie_name = getattr(settings, 'CSRF_COOKIE_NAME', None)
    csrf_cookie_name_path = getattr(settings, 'CSRF_COOKIE_PATH', '/')
    auth_cookie_name_path = getattr(settings, 'JWT_AUTH_COOKIE_PATH', '/')
    refresh_cookie_name = getattr(settings, 'JWT_AUTH_REFRESH_COOKIE', None)
    refresh_cookie_path = getattr(settings, 'JWT_AUTH_REFRESH_COOKIE_PATH', '/')

    if(auth_cookie_name):
        response.delete_cookie(auth_cookie_name, path=auth_cookie_name_path)
    if(csrf_cookie_name):
        response.delete_cookie(csrf_cookie_name, path=csrf_cookie_name_path)
    if(refresh_cookie_name):
        response.delete_cookie(refresh_cookie_name, path=refresh_cookie_path)
