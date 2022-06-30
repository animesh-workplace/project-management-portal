from django.urls import path
from .modules.create import CreateSampleIdentifier
from .modules.upload_projectsdata import (
    Getdata,
    CreateProjectsdata,
)

urlpatterns = [
    path(
        "create/",
        CreateSampleIdentifier.as_view(),
        name="create-sample-identifier-api",
    ),
    path("getmodelsdata/", Getdata.as_view(), name="getmodelsdata"),
    path(
        "uploadprojectsdata/", CreateProjectsdata.as_view(), name="createprojectsdata"
    ),
]
