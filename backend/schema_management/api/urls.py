from django.urls import path, include
from .modules.project_names import ProjectNamesView
from .modules.project_info import ProjectDetailView
from .modules.metadata_info import MetadataDetailView
from .modules.metadata_names import MetadataNamesView
from .modules.upload_project import UploadProjectView
from .modules.create_project import CreateProjectView
from .modules.upload_metadata import UploadMetadataView
from .modules.create_metadata import CreateMetadataView

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
                path("info/", MetadataDetailView.as_view(), name="metadata-info-api"),
                path("names/", MetadataNamesView.as_view(), name="metadata-names-api"),
            ]
        ),
    ),
    path(
        "projects/",
        include(
            [
                path("create/", CreateProjectView.as_view(), name="create-project-api"),
                path("upload/", UploadProjectView.as_view(), name="upload-project-api"),
                path("info/", ProjectDetailView.as_view(), name="project-info-api"),
                path("names/", ProjectNamesView.as_view(), name="project-names-api"),
            ]
        ),
    ),
]
