from django.urls import path, include
from .modules.send_request import SendRequestView
from .modules.handle_request import HandleRequestView

urlpatterns = [
    path("request/", SendRequestView.as_view(), name="send-request-api"),
    path("handle/", HandleRequestView.as_view(), name="handle-request-api"),
]
