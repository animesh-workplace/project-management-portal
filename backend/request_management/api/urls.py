from django.urls import path, include
from .modules.request_project import UserRequestApi

urlpatterns = [
    path("request/", UserRequestApi.as_view(), name="request-project-api"),
]
