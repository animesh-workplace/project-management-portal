from django.urls import path
from .modules.create import CreateView

# from .modules.upload_projectsdata import (
#     Getdata,
#     CreateProjectsdata,
# )

urlpatterns = [
    path("create/", CreateView.as_view(), name="create-api"),
    #
    # path("getmodelsdata/", Getdata.as_view(), name="getmodelsdata"),
    # path(
    #     "uploadprojectsdata/", CreateProjectsdata.as_view(), name="createprojectsdata"
    # ),
]
