from django.urls import path, include
from .modules.request_project import UserRequestView

urlpatterns = [
    path("request/", UserRequestView.as_view(), name="request-project-api"),
]
