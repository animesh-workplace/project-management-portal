from django.urls import path, include
from .modules.create_project import CreateProjectView
from .modules.create_metadata import CreateMetadataView
from .modules.upload_project import UploadProjectView
from .modules.upload_metadata import UploadMetadataView
from .modules.views import ProjectDetailView

# from schema_management.api.modules.upload_project_data

urlpatterns = [
    path(
        "metadata/",
        include(
            [
                path(
                    "create/", CreateMetadataView.as_view(), name="create-metadata-api"
                ),
                path(
                    "upload/", UploadMetadataView.as_view(), name="create-metadata-api"
                ),
            ]
        ),
    ),
    path(
        "projects/",
        include(
            [
                path("create/", CreateProjectView.as_view(), name="create-project-api"),
                path("upload/", UploadProjectView.as_view(), name="upload-project-api"),
            ]
        ),
    ),
]
