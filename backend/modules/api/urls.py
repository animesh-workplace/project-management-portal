from django.urls import path
from modules.api.modules.createmodule import CreateModules
from modules.api.modules.upload_modulesdata import GetModuledata, CreateModuledata

urlpatterns = [
    path("create_module/", CreateModules.as_view(), name="create_module"),
    path("uploadmoduledata/", CreateModuledata.as_view(), name="uploadmoduledata"),
    path("getmoduledata/", GetModuledata.as_view(), name="getmoduledata"),
]
