from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from authentication.api.utils import create_uniform_response
from schema_management.models import MetadataHandler, ProjectHandler
from rest_framework import generics, exceptions, serializers, status


class CreateMetadataSerializer(serializers.Serializer):
    name = serializers.CharField()
    config = serializers.JSONField()
    project = serializers.CharField()

    class Meta:
        fields = None

    def validate_name(self, name):
        qs = ModelSchema.objects
        model_name = f"{name.lower()}_si"
        if qs.filter(name__iexact=model_name).exists():
            raise exceptions.ValidationError("Already exists")
        return name

    def validate(self, value):
        name = value.get("name")
        config = value.get("config")
        model_name = f"{name.lower()}_si"
        model_schema = self.create_model(model_name)
        MetadataHandler.objects.create(name=model_name, config=config)
        self.register_model(model_schema)
        return value


class CreateMetadataView(generics.GenericAPIView):
    queryset = MetadataHandler
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
            "message": "Metadata creation Successful",
        }
        response = Response(data, status=status.HTTP_200_OK)
        return response
