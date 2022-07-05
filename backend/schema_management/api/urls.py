from django.urls import path, include
from .modules.create_project import CreateProjectView
from .modules.create_metadata import CreateMetadataView
from .modules.upload_project_data import UploadProjectView, UploadMetadataView

# from schema_management.api.modules.upload_project_data

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
    path(
        "projects/",
        include(
            [
                path(
                    "upload_project_data/",
                    UploadProjectView.as_view(),
                    name="upload-project-data-api",
                )
            ]
        ),
    ),
    path(
        "metadata/",
        include(
            [
                path(
                    "upload_metadata/",
                    UploadMetadataView.as_view(),
                    name="upload-metadata-api",
                )
            ]
        ),
    ),
]
