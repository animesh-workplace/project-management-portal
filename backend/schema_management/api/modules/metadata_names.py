from django.apps import apps
from rest_framework.response import Response
from schema_management.models import MetadataHandler
from rest_framework.permissions import IsAuthenticated
from user_management.api.utils import create_uniform_response
from rest_framework import generics, exceptions, serializers, status


class MetadataNamesSerializer(serializers.Serializer):
    class Meta:
        fields = "__all__"

    def validate(self, value):
        user = self.context["request"].user
        metadata_model = self.context["view"].get_queryset()
        # donot use single letter variables
        metadata = [
            v
            for k, v in metadata_model.items()
            if k.startswith(user.username.lower()) and k.endswith("metadata")
        ]
        response = {}
        response["metadata"] = [str(i).split(".")[2][0:-2] for i in metadata]
        return response


class MetadataNamesView(generics.GenericAPIView):
    queryset = apps.get_app_config("table_factory").models
    serializer_class = MetadataNamesSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        if self.serializer.is_valid():
            return Response(self.serializer.validated_data)
        return Response(
            create_uniform_response(self.serializer.errors),
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )
