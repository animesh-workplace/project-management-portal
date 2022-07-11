from django.urls import path, include
from .modules.request_project import UserRequestView
from .modules.accept_project import ProjectPermissionsView

urlpatterns = [
    path("request/", UserRequestView.as_view(), name="request-project-api"),
    path("accept/", ProjectPermissionsView.as_view(), name="accept-project-api"),
]
