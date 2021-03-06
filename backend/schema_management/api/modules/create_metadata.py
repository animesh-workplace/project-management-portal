from django.utils.text import slugify
from rest_framework.response import Response
from table_factory.api.tasks import CreateTable
from rest_framework.permissions import IsAuthenticated
from user_management.api.utils import create_uniform_response
from schema_management.models import MetadataHandler, ProjectHandler
from rest_framework import generics, exceptions, serializers, status


class CreateMetadataSerializer(serializers.Serializer):
    name = serializers.CharField()
    config = serializers.JSONField()
    project = serializers.CharField()

    class Meta:
        fields = None

    def validate_project(self, project):
        user = self.context["request"].user
        table_name = self.get_name("project", user, project)
        # Check if the name exists in the ProjectHandler database
        if ProjectHandler.objects.filter(table_name__iexact=table_name).exists():
            return project
        raise exceptions.ValidationError("Project doesnot exists")

    def check_name(self, user, project, name):
        table_name = self.get_name("metadata", user, project, name)
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
        project = value.get("project")
        user = self.context["request"].user
        if self.check_name(user, project, name):
            table_name = self.get_name("metadata", user, project, name)
            project_instance = self.get_project(self.get_name("project", user, project))
            self.create_table(table_name, config)
            self.context["view"].get_queryset().objects.create(
                name=name,
                config=config,
                table_name=table_name,
                project_name=project_instance,
            )
            return value

    @staticmethod
    def get_project(project_name):
        return ProjectHandler.objects.get(table_name__iexact=project_name)

    @staticmethod
    def get_name(table_type, user, project, metadata=None):
        if table_type == "project":
            return f"{user}_{slugify(project).replace('-', '_')}_si"
        if table_type == "metadata":
            return f"{user}_{slugify(project).replace('-', '_')}_{slugify(metadata).replace('-', '_')}_metadata"
        raise exceptions.ValidationError("Invalid Type: Get name -> Metadata")

    @staticmethod
    def create_table(table_name, config):
        CreateTable(table_name, config)
        # Calls the function for creating the project table in MetadataFactory
        # It should return true/false
        # pass


class CreateMetadataView(generics.GenericAPIView):
    queryset = MetadataHandler
    permission_classes = [IsAuthenticated]
    serializer_class = CreateMetadataSerializer

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
