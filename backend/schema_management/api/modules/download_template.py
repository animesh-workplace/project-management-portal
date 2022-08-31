import re
import csv
import datetime
import datetime as dt
from django.utils.text import slugify
from backend.settings import BASE_DIR
from rest_framework.response import Response
from table_factory.api.tasks import CreateTable
from rest_framework.permissions import IsAuthenticated
from user_management.api.utils import create_uniform_response
from rest_framework import generics, exceptions, serializers, status
from schema_management.models import ProjectHandler, MetadataHandler

file_name = str(datetime.datetime.today())
new_file = re.sub("[ ;:]", "_", file_name)
path = (
    f"{BASE_DIR}/downloads/projects_templates/sample_identifier_template{new_file}.csv"
)
# metadatapath = (
#     f"{BASE_DIR}/downloads/metadata_templates/{metadataname}{new_file}template.csv"
# )
# f_name = f"sample_identifier_template{new_file}.csv"


class DownloadProjectTemplateSerializer(serializers.Serializer):
    name = serializers.CharField()

    class Meta:
        fields = ("config",)

    def validate_name(self, name):
        tablename = f"{self.context['request'].user}_{name}_si"
        if (
            self.context["view"]
            .get_queryset()
            .objects.filter(table_name__iexact=tablename)
            .exists()
        ):
            return name
        raise exceptions.ValidationError("Sample identifier is not exists")

    def validate(self, value):
        name = value.get("name")
        tablename = f"{self.context['request'].user}_{name}_si"
        queryset = (
            self.context["view"]
            .get_queryset()
            .objects.filter(table_name__iexact=tablename)
            .values_list("config", flat=True)[0]
        )
        path = f"{BASE_DIR}/downloads/projects_templates/{name}{new_file}_template.csv"
        template_columns = []
        for i in queryset:
            template_columns.append(i["name"])
        with open(path, "w", encoding="UTF8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(template_columns)
        return path


class DownloadProjectTemplate(generics.GenericAPIView):
    queryset = ProjectHandler
    serializer_class = DownloadProjectTemplateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        if self.serializer.is_valid():
            return Response(self.serializer.validated_data)
        return Response(
            create_uniform_response(self.serializer.errors),
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )


class DownloadMetadataTemplateSerializer(serializers.Serializer):
    name = serializers.CharField()
    project = serializers.CharField()

    class Meta:
        fields = ("config",)

    def validate_name(self, name):
        if (
            self.context["view"]
            .get_queryset()
            .objects.filter(name__iexact=name)
            .exists()
        ):
            return name
        raise exceptions.ValidationError("Meatadata is not exists")

    def validate_project(self, project):
        tablename = f"{self.context['request'].user}_{project}_si"
        if ProjectHandler.objects.filter(table_name__iexact=tablename).exists():
            return project
        raise exceptions.ValidationError("Sample identifier is not exists")

    def validate(self, value):
        name = value.get("name")
        project = value.get("project")
        tablename = f"{self.context['request'].user}_{project}_{name}_metadata"
        queryset = (
            self.context["view"]
            .get_queryset()
            .objects.filter(table_name__iexact=tablename)
            .values_list("config", flat=True)[0]
        )
        metadatapath = f"{BASE_DIR}/downloads/metadata_templates/{project}_{name}{new_file}template.csv"
        template_columns = []
        for i in queryset:
            template_columns.append(i["name"])
        with open(metadatapath, "w", encoding="UTF8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(template_columns)
        return metadatapath


class DownloadMetadataTemplate(generics.GenericAPIView):
    queryset = MetadataHandler
    serializer_class = DownloadMetadataTemplateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        if self.serializer.is_valid():
            return Response(self.serializer.validated_data)
        return Response(
            create_uniform_response(self.serializer.errors),
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )
