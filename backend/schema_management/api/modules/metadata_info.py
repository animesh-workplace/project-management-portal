from django.apps import apps
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from user_management.api.utils import create_uniform_response
from rest_framework import generics, exceptions, serializers, status
from schema_management.models import MetadataHandler, ProjectHandler
import datetime
from datetime import datetime


class MetadataDetailSerializer(serializers.Serializer):
    name = serializers.CharField()
    m_id = serializers.IntegerField()

    class Meta:
        fields = "__all__"

    def validate(self, value):
        name = value.get("name").lower()
        m_id = value.get("m_id")
        metadata_model = self.context["view"].get_queryset()[name.lower()]
        if (
            not self.context["view"]
            .get_queryset()[name.lower()]
            .objects.filter(id=m_id)
            .exists()
        ):
            temp = {}
            for k in metadata_model._meta.fields:
                temp[str(k).split(".")[-1]] = ""
            return temp
        if MetadataHandler.objects.filter(table_name__iexact=name).exists():
            config = list(
                MetadataHandler.objects.filter(table_name__iexact=name).values_list(
                    "config", flat=True
                )
            )[0]
            dateFields = [k["name"].lower() for k in config if k["data_type"] == "date"]
            queryset = metadata_model.objects.values().get(id=m_id)
            queryset = {
                k: (str(v).split(" ")[0] if k in dateFields else v)
                for (k, v) in queryset.items()
            }
            return queryset
        raise exceptions.ValidationError(f"{name} is not exists in metadata_model")


class MetadataDetailView(generics.GenericAPIView):
    queryset = apps.get_app_config("table_factory").models
    serializer_class = MetadataDetailSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        if self.serializer.is_valid():
            return Response(self.serializer.validated_data)
        return Response(
            create_uniform_response(self.serializer.errors),
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )


class MetadataDetailSerializer1(serializers.Serializer):
    name = serializers.CharField()
    m_id = serializers.CharField()

    class Meta:
        fields = "__all__"

    def validate(self, value):
        name = value.get("name").lower()
        m_id = value.get("m_id")

        print(name.split("_")[1])
        config_table_name = f"{name.split('_')[0]}_{name.split('_')[1]}_si".lower()

        config_data = list(
            ProjectHandler.objects.filter(
                table_name__iexact=config_table_name
            ).values_list("config", flat=True)
        )[0]
        unique_key = f'{next(filter(lambda i: i["unique"] == "True", config_data))["name"]}_id'.lower()
        print(unique_key)
        metadata_model = self.context["view"].get_queryset()[name.lower()]
        if (
            not self.context["view"]
            .get_queryset()[name.lower()]
            .objects.filter(**{unique_key: m_id})
            .exists()
        ):
            temp = {}
            for k in metadata_model._meta.fields:
                temp[str(k).split(".")[-1]] = ""
            return temp
        if MetadataHandler.objects.filter(table_name__iexact=name).exists():
            config = list(
                MetadataHandler.objects.filter(table_name__iexact=name).values_list(
                    "config", flat=True
                )
            )[0]
            dateFields = [k["name"].lower() for k in config if k["data_type"] == "date"]
            queryset = metadata_model.objects.values().get(**{unique_key: m_id})
            queryset = {
                k: (str(v).split(" ")[0] if k in dateFields else v)
                for (k, v) in queryset.items()
            }
            return queryset
        raise exceptions.ValidationError(f"{name} is not exists in metadata_model")


class MetadataDetailView1(generics.GenericAPIView):
    queryset = apps.get_app_config("table_factory").models
    serializer_class = MetadataDetailSerializer1
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        if self.serializer.is_valid():
            return Response(self.serializer.validated_data)
        return Response(
            create_uniform_response(self.serializer.errors),
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )
