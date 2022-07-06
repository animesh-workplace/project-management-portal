from .utils import get_name
from rest_framework.response import Response
from table_factory.api.tasks import CreateTable
from schema_management.models import ProjectHandler
from rest_framework.permissions import IsAuthenticated
from user_management.api.utils import create_uniform_response
from rest_framework import generics, exceptions, serializers, status


class CreateProjectSerializer(serializers.Serializer):
    name = serializers.CharField()
    config = serializers.JSONField()

    class Meta:
        fields = None

    def validate_name(self, name):
        user = self.context["request"].user
        table_name = get_name("project", user, name)
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
        table_name = get_name("project", user, name)
        self.create_table(table_name, config)
        self.context["view"].get_queryset().objects.create(
            name=name, config=config, table_name=table_name
        )
        return value

    @staticmethod
    def create_table(table_name, config):
        CreateTable(table_name, config)
        # if create_project_table(table_name, config):
        # return true
        # else:
        #     raise exceptions.ValidationError("Some errror during creation")
        # Calls the function for creating the project table in ProjectFactory
        # It should return true/false
        # pass


class CreateProjectView(generics.GenericAPIView):
    queryset = ProjectHandler
    permission_classes = [IsAuthenticated]
    serializer_class = CreateProjectSerializer

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
