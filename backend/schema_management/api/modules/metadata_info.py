from django.apps import apps
from rest_framework.response import Response
from schema_management.models import MetadataHandler
from rest_framework.permissions import IsAuthenticated
from user_management.api.utils import create_uniform_response
from rest_framework import generics, exceptions, serializers, status


class MetadataDetailSerializer(serializers.Serializer):
    name = serializers.CharField()
    m_id = serializers.IntegerField()

    class Meta:
        fields = "__all__"

    def validate(self, value):
        name = value.get("name").lower()
        m_id = value.get("m_id")
        if (
            not self.context["view"]
            .get_queryset()[name.lower()]
            .objects.filter(id=m_id)
            .exists()
        ):
            raise exceptions.ValidationError("metadata is not exists")
        if MetadataHandler.objects.filter(table_name=name).exists():
            metadata_model = self.context["view"].get_queryset()[name.lower()]
            queryset = metadata_model.objects.values().get(id=m_id)
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
