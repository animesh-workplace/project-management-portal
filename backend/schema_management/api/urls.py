from django.urls import path, include
from .modules.get_config import ProjectConfigView
from .modules.get_config import MetadataConfigView
from .modules.project_names import ProjectNamesView
from .modules.project_info import ProjectDetailView
from .modules.metadata_info import MetadataDetailView
from .modules.metadata_names import MetadataNamesView
from .modules.upload_project import UploadProjectView
from .modules.create_project import CreateProjectView
from .modules.update_project import UpdateProjectView
from .modules.upload_metadata import UploadMetadataView
from .modules.create_metadata import CreateMetadataView
from .modules.update_metadata import UpdateMetadataView
from .modules.delete_metadata import DeleteMeatadataView
from .modules.remove_project_info import DeleteProjectView


urlpatterns = [
    path(
        "metadata/",
        include(
            [
                path(
                    "create/", CreateMetadataView.as_view(), name="create-metadata-api"
                ),
                path(
                    "config/", MetadataConfigView.as_view(), name="metadata-config-api"
                ),
                path(
                    "upload/", UploadMetadataView.as_view(), name="create-metadata-api"
                ),
                path(
                    "update/", UpdateMetadataView.as_view(), name="update-metadata-api"
                ),
                path("info/", MetadataDetailView.as_view(), name="metadata-info-api"),
                path("names/", MetadataNamesView.as_view(), name="metadata-names-api"),
                path(
                    "delete/", DeleteMeatadataView.as_view(), name="delete-metadata-api"
                ),
            ]
        ),
    ),
    path(
        "projects/",
        include(
            [
                path("create/", CreateProjectView.as_view(), name="create-project-api"),
                path("config/", ProjectConfigView.as_view(), name="project-config-api"),
                path("upload/", UploadProjectView.as_view(), name="upload-project-api"),
                path("update/", UpdateProjectView.as_view(), name="update-project-api"),
                path("info/", ProjectDetailView.as_view(), name="project-info-api"),
                path("names/", ProjectNamesView.as_view(), name="project-names-api"),
                path(
                    "delete/", DeleteProjectView.as_view(), name="delete-metadata-api"
                ),
            ]
        ),
    ),
]
