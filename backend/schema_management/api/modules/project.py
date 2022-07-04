from django.utils.text import slugify
from rest_framework.response import Response
from schema_management.models import ProjectHandler
from rest_framework.permissions import IsAuthenticated
from project_factory.api.tasks import create_project_table
from authentication.api.utils import create_uniform_response
from rest_framework import generics, exceptions, serializers, status


class CreateProjectSerializer(serializers.Serializer):
    name = serializers.CharField()
    config = serializers.JSONField()

    class Meta:
        fields = None

    def validate_name(self, name):
        user = self.context["request"].user
        table_name = self.get_name("project", user, name)
        # Check if the name exists in the queryset database
        if (
            self.context["view"]
            .get_queryset()
            .objects.filter(table_name__iexact=table_name)
            .exists()
        ):
            raise exceptions.ValidationError("Already exists")
        return name

    def validate(self, value):
        name = value.get("name")
        config = value.get("config")
        user = self.context["request"].user
        table_name = self.get_name("project", user, name)
        if self.create_table(table_name):
            self.context["view"].get_queryset().objects.create(
                name=name, config=config, table_name=table_name
            )
        # Incase of false handle the response
        return value

    @staticmethod
    def get_name(table_type, user, project, metadata=None):
        if table_type == "project":
            return f"{user}_{slugify(project).replace('-', '_')}_si"
        if table_type == "metadata":
            return f"{user}_{slugify(project)..replace('-', '_')}_{slugify(metadata).replace('-', '_')}_metadata"
        raise exceptions.ValidationError("Invalid Type: Get name -> Project")

    @staticmethod
    def create_table(table_name, config):
        if create_project_table(table_name, config):
            return true
        else:
            raise exceptions.ValidationError("Some errror during creation")
        # Calls the function for creating the project table in ProjectFactory
        # It should return true/false
        # pass


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
