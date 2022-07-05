from django.db import models
from django.conf import settings
from django.contrib import admin
from rest_framework import generics
from rest_framework import exceptions
from rest_framework import serializers
from projects.models import Projectname
from django.urls import clear_url_caches
from importlib import import_module, reload
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from projects.models import ModelSchema, FieldSchema
from rest_framework.permissions import IsAuthenticated, AllowAny


class DataSerializer(serializers.Serializer):
    model_data = serializers.ListField()
    projectname = serializers.CharField()


class CreateModels(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DataSerializer

    def post(self, request, *args, **kwargs):
        modelExists = False
        modelCreated = False
        projectName = ""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        projectName = serializer.validated_data["projectname"]
        projectName = projectName.lower()
        model_data = serializer.validated_data["model_data"]
        username = self.request.user.username
        print(username)
        try:
            model_schema = ModelSchema.objects.create(
                name=username + "_" + projectName + "_" + "sample_identifier"
            )
            modelCreated = True
        except Exception as e:
            modelExists = True
            return Response(
                {
                    "modelExists": modelExists,
                    "modelCreated": modelCreated,
                    "modelName": projectName,
                }
            )
        for row in model_data:
            if row["datatype"] == "radio":
                FieldSchema.objects.create(
                    name=row["field"],
                    data_type="character",
                    max_length=row["maxlen"],
                    model_schema=model_schema,
                    null=row["null"],
                    unique=row["unique"],
                )
            else:
                FieldSchema.objects.create(
                    name=row["field"],
                    data_type=row["datatype"],
                    max_length=row["maxlen"],
                    model_schema=model_schema,
                    null=row["null"],
                    unique=row["unique"],
                )
        Projectname.objects.create(
            modelname=username + "_" + projectName + "_" + "sample_identifier",
            config_file=model_data,
        )
        reg_model = model_schema.as_model()
        admin.site.register(reg_model)
        reload(import_module(settings.ROOT_URLCONF))
        clear_url_caches()
        return Response(
            {
                "modelExists": modelExists,
                "modelCreated": modelCreated,
                "modelName": projectName,
            }
        )
