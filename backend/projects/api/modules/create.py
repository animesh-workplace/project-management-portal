from django.conf import settings
from django.contrib import admin
from projects.models import Projectname
from django.urls import clear_url_caches
from django.db.utils import IntegrityError
from importlib import import_module, reload
from rest_framework.response import Response
from projects.models import ModelSchema, FieldSchema
from rest_framework.permissions import IsAuthenticated
from authentication.api.utils import create_uniform_response
from rest_framework import generics, exceptions, serializers, status


class CreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    config = serializers.JSONField()

    class Meta:
        fields = None

    def validate(self, value):
        name = value.get("name")
        config = value.get("config")
        model_name = f"{name.lower()}_sample_identifier"
        model_schema = self.create_model(model_name)
        self.create_model_fields(model_schema, config)
        Projectname.objects.create(modelname=model_name, config_file=config)
        self.register_model(model_schema)
        return value

    @staticmethod
    def create_model(model_name):
        try:
            model_schema = ModelSchema.objects.create(name=model_name)
            return model_schema
        except Exception as e:
            # Handle exception in a better way
            raise serializers.ValidationError(
                {"Error": "Model already exists"}, code="natural"
            )

    @staticmethod
    def create_model_fields(model_schema, config):
        for item in config:
            # Might require a try and catch block
            FieldSchema.objects.create(
                null=item["null"],
                name=item["field"],
                unique=item["unique"],
                max_length=item["maxlen"],
                model_schema=model_schema,
                data_type="character"
                if (item["datatype"] == "radio")
                else item["datatype"],
            )
            # might need to return something

    @staticmethod
    def register_model(model_schema):
        model = model_schema.as_model()
        admin.site.register(model)
        reload(import_module(settings.ROOT_URLCONF))
        clear_url_caches()


class CreateView(generics.GenericAPIView):
    queryset = Projectname
    serializer_class = CreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        if self.serializer.is_valid():
            return self.get_response()
        return Response(
            create_uniform_response(self.serializer.errors),
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )

    def get_response(self):
        data = {
            "code": "SUCCESS",
            "message": "Project creation Successful",
        }
        response = Response(data, status=status.HTTP_200_OK)
        return response
