from django.urls import path
from .modules.module import CreateMetadataView
from .modules.project import CreateProjectView

urlpatterns = [
    path(
        "metadata/",
        include(
            [path("create/", CreateMetadataView.as_view(), name="create-metadata-api")]
        ),
    ),
    path(
        "projects/",
        include(
            [path("create/", CreateProjectView.as_view(), name="create-project-api")]
        ),
    ),
]
