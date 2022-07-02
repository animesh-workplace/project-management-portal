from django.urls import path
from .modules.module import CreateModuleView
from .modules.project import CreateProjectView

urlpatterns = [
    path("modules/", CreateModuleView.as_view(), name="create-module-api"),
    path("projects/", CreateProjectView.as_view(), name="create-project-api"),
]
