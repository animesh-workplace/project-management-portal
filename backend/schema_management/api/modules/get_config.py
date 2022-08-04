from django.apps import apps
from rest_framework.response import Response
from table_factory.api.tasks import UploadData
from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from user_management.api.utils import create_uniform_response
from rest_framework import generics, exceptions, serializers, status
from schema_management.models import ProjectHandler, MetadataHandler


class ProjectConfigSerializer(serializers.Serializer):
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
        return queryset


class ProjectConfigView(generics.GenericAPIView):
    queryset = ProjectHandler
    serializer_class = ProjectConfigSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        if self.serializer.is_valid():
            return Response(self.serializer.validated_data)
        return Response(
            create_uniform_response(self.serializer.errors),
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )


class MetadataConfigSerializer(serializers.Serializer):
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
        return queryset


class MetadataConfigView(generics.GenericAPIView):
    queryset = MetadataHandler
    serializer_class = MetadataConfigSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        if self.serializer.is_valid():
            return Response(self.serializer.validated_data)
        return Response(
            create_uniform_response(self.serializer.errors),
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )