from django.urls import path, include
from .modules.project import CreateProjectView
from .modules.metadata import CreateMetadataView

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
