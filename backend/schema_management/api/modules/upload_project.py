import itertools
from .utils import get_name
from django.apps import apps
from rest_framework.response import Response
from rest_framework import generics, serializers
from table_factory.api.tasks import UploadProjectData
from rest_framework.permissions import IsAuthenticated
from user_management.api.utils import create_uniform_response
from schema_management.models import ProjectHandler, MetadataHandler
from rest_framework import generics, exceptions, serializers, status


class UploadProjectSerializer(serializers.Serializer):
    data = serializers.JSONField()
    name = serializers.CharField()

    class Meta:
        fields = None

    def validate_name(self, name):
        user = self.context["request"].user
        table_name = get_name("project", user, name)
        # Check if the name exists in the queryset database
        if ProjectHandler.objects.filter(table_name__iexact=table_name).exists():
            return name
        raise exceptions.ValidationError("Table doesn't exists")

    def validate(self, value):
        name = value.get("name")
        data = value.get("data")
        user = self.context["request"].user
        table_name = get_name("project", user, name)
        instance = self.context["view"].get_queryset()[table_name]
        project_config = (
            ProjectHandler.objects.filter(table_name=table_name)
            .values_list("config", flat=True)
            .first()
        )
        # Need to add required column in the config
        required_columns = {col["name"] for col in project_config if (col["required"])}
        self.check_required_columns(required_columns, data)
        self.check_radio_options("radio", project_config, data)
        self.check_radio_options("multiradio", project_config, data)
        self.upload_table(table_name, data, instance)
        return value

    @staticmethod
    def check_required_columns(columns, data):
        # If there are no required columns get return back
        if not columns:
            return
        for (index, row) in enumerate(data):
            # Check whether the required columns are subset of the columns in the data
            if not columns.issubset(set(row.keys())):
                raise exceptions.ValidationError(
                    f"Row index {index} requires column {columns - set(row.keys())}"
                )

    @staticmethod
    def check_radio_options(radiotype, config, data):
        for row in config:
            if row["data_type"] == "radio" or row["data_type"] == "multiradio":
                if radiotype == "radio":
                    # If radio then only one option
                    data_choices = {i[row["name"]] for i in data}
                elif radiotype == "multiradio":
                    # If multiradio then we get list of list
                    temp = [i[row["name"]] for i in data]
                    data_choices = set(itertools.chain(*temp))
                # Checking if the unique options from the data is a subset of the options in the config
                if not data_choices.issubset(set(row["options"])):
                    raise exceptions.ValidationError(
                        f"{row['name']} doesnot have valid option {data_choices - set(row['options'])}"
                    )

    @staticmethod
    def upload_table(name, data, instance):
        UploadProjectData(name, data, instance)


class UploadProjectView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UploadProjectSerializer
    queryset = apps.get_app_config("table_factory").models

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
            "message": "Sample added successfully",
        }
        response = Response(data, status=status.HTTP_200_OK)
        return response
