from rest_framework.response import Response
from schema_management.models import ProjectHandler
from rest_framework.permissions import IsAuthenticated
from authentication.api.utils import create_uniform_response
from rest_framework import generics, exceptions, serializers, status


class CreateProjectSerializer(serializers.Serializer):
    name = serializers.CharField()
    config = serializers.JSONField()

    class Meta:
        fields = None

    def validate_name(self, name):
        qs = ModelSchema.objects
        # model_name = f"{name.lower()}_si"
        # Check if the name exists in the queyset database
        # self.context['view'].get_queryset().objects.values_list('Sample_Barcode', flat = True)
        if qs.filter(name__iexact=model_name).exists():
            raise exceptions.ValidationError("Already exists")
        return name

    def validate(self, value):
        name = value.get("name")
        config = value.get("config")
        model_name = f"{name.lower()}_si"
        model_schema = self.create_model(model_name)
        ProjectHandler.objects.create(name=model_name, config=config)
        self.register_model(model_schema)
        return value


class CreateProjectView(generics.GenericAPIView):
    queryset = ProjectHandler
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
