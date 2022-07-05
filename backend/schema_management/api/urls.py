from django.urls import path, include
from .modules.create_project import CreateProjectView
from .modules.create_metadata import CreateMetadataView

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
