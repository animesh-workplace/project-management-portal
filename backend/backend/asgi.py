"""
ASGI config for backend project.
It exposes the ASGI callable as a module-level variable named ``application``.
"""
import os
from channels.routing import (
    URLRouter,
    ProtocolTypeRouter,
    get_default_application,
)
from django.core.asgi import get_asgi_application
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
asgi_app = get_asgi_application()

from dotenv import load_dotenv
from django.urls import re_path
from django.conf import settings
from .token_auth import JWTAuthMiddleware
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator


load_dotenv(settings.BASE_DIR / ".env")

application = ProtocolTypeRouter(
    {
        "http": asgi_app,
        # "websocket": AllowedHostsOriginValidator(
        #     JWTAuthMiddleware(
        #         URLRouter(
        #             [
        #                 # re_path(os.getenv('BASE_URL'), URLRouter([
        #                 # re_path(r'^wsa/backend/$', BackendConsumer.as_asgi(), name='backend-consumer'),
        #                 # re_path(r'^wsa/frontend/$', FrontendConsumer.as_asgi(), name='frontend-consumer'),
        #                 # ]))
        #             ]
        #         )
        #     )
        # ),
    }
)
