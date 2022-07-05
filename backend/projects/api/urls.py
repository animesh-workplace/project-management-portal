from django.urls import path
from projects.api.modules.createmodel import CreateModels

from projects.api.modules.upload_projectsdata import (
    Getdata,
    CreateProjectsdata,
)

urlpatterns = [
    path("create_model/", CreateModels.as_view(), name="create_model"),
    path("getmodelsdata/", Getdata.as_view(), name="getmodelsdata"),
    # path("postdata/", Postdata.as_view(), name="postdata"),
    # path("getmoduledata/", GetModuledata.as_view(), name="getmoduledata"),
    path(
        "uploadprojectsdata/", CreateProjectsdata.as_view(), name="createprojectsdata"
    ),
    # path("createmoduledata/", CreateModuledata.as_view(), name="createmoduledata"),
]
