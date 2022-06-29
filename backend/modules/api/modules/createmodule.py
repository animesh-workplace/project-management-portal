from django.db import models
from django.conf import settings
from django.contrib import admin
from rest_framework import generics
from rest_framework import exceptions
from rest_framework import serializers
from modules.models import Modulename
from projects.models import Projectname
from django.urls import clear_url_caches
from importlib import import_module, reload
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from modules.models import ModuleModelSchema, ModuleFieldSchema


class ModuleSerializer(serializers.Serializer):
    module_data = serializers.ListField()
    modulename = serializers.CharField()
    projectname = serializers.CharField()


class CreateModules(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = ModuleSerializer

    def post(
        self,
        request,
        *args,
        **kwargs,
    ):
        moduleExists = False
        moduleCreated = False
        moduleName = ""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        projectName = serializer.validated_data["projectname"]
        projectName = projectName.lower()
        projectTablename = projectName + "_" + "sample_identifier"
        moduleName = (
            projectName + "_" + serializer.validated_data["modulename"] + "_" + "module"
        )
        moduleName = moduleName.lower()
        module_data = serializer.validated_data["module_data"]
        models = list(Projectname.objects.values_list("modelname", flat=True))
        # radio = "radio"
        if projectTablename in models:
            try:
                module_schema = ModuleModelSchema.objects.create(name=moduleName)
                moduleCreated = True
            except Exception as e:
                moduleExists = True
                return Response(
                    {
                        "moduleExists": moduleExists,
                        "moduleCreated": moduleCreated,
                        "moduleName": moduleName,
                    }
                )
            for row in module_data:
                if row["datatype"] == "radio":
                    ModuleFieldSchema.objects.create(
                        name=row["field"],
                        data_type="character",
                        max_length=row["maxlen"],
                        module_schema=module_schema,
                        null=row["null"],
                        unique=row["unique"],
                    )
                else:
                    ModuleFieldSchema.objects.create(
                        name=row["field"],
                        data_type=row["datatype"],
                        max_length=row["maxlen"],
                        module_schema=module_schema,
                        null=row["null"],
                        unique=row["unique"],
                    )
            Modulename.objects.create(
                projectname_id=projectTablename,
                modulename=moduleName,
                config_file=module_data,
            )
            reg_model = module_schema.as_model()
            admin.site.register(reg_model)
            reload(import_module(settings.ROOT_URLCONF))
            clear_url_caches()
            return Response(
                {
                    "moduleExists": moduleExists,
                    "moduleCreated": moduleCreated,
                    "moduleName": moduleName,
                }
            )
        return Response(
            {
                "projectExists": False,
                "moduleCreated": moduleCreated,
                "moduleName": moduleName,
            }
        )
