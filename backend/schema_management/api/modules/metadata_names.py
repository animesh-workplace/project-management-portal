from django.apps import apps
from rest_framework.response import Response
from schema_management.models import MetadataHandler
from rest_framework.permissions import IsAuthenticated
from user_management.api.utils import create_uniform_response
from rest_framework import generics, exceptions, serializers, status


class MetadataNamesSerializer(serializers.Serializer):
    # This requires project name to be given based on which the metadata names are given back
    project_name = serializers.CharField()

    class Meta:
        fields = "__all__"

    def validate(self, value):
        user = self.context["request"].user
        project_name = value.get("project_name")
        metadata_names = (
            self.context["view"]
            .get_queryset()
            .objects.values_list("name", flat=True)
            .filter(table_name__startswith=user.username + "_" + project_name)
        )
        return metadata_names


class MetadataNamesView(generics.GenericAPIView):
    queryset = MetadataHandler
    serializer_class = MetadataNamesSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        if self.serializer.is_valid():
            return Response({"metadata": self.serializer.validated_data})
        return Response(
            create_uniform_response(self.serializer.errors),
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )
