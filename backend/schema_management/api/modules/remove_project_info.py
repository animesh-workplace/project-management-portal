from django.apps import apps
from rest_framework.response import Response
from schema_management.models import ProjectHandler, MetadataHandler
from rest_framework.permissions import IsAuthenticated
from user_management.api.utils import create_uniform_response
from rest_framework import generics, exceptions, serializers, status


class DeletePostSerializer(serializers.Serializer):
    # rename id to something else id is a restricted keyword
    pk = serializers.IntegerField()
    name = serializers.CharField()

    class Meta:
        fields = "__all__"

    def validate(self, value):
        pk = value.get("pk")
        name = value.get("name")
        if not name in list(
            ProjectHandler.objects.values_list("table_name", flat=True).filter(
                table_name=name
            )
        ):
            raise exceptions.ValidationError("Project is not exists")
        app_model = self.context["view"].get_queryset()[name.lower()]
        pk_list = list(app_model.objects.values_list("id", flat=True))
        if pk not in pk_list:
            raise exceptions.ValidationError("Primary key is not exists")

        # Get the list of metadata tables which are from given sample identifier
        metadata_tables = list(
            MetadataHandler.objects.values_list("name", flat=True).filter(
                project_name_id=name.lower()
            )
        )

        # Get config file of given project to identifying the first unique key
        config = list(
            ProjectHandler.objects.values_list("config", flat=True).filter(
                table_name=name
            )
        )[0]
        unique_key = next(filter(lambda i: i["unique"] == "True", config))

        # Get first unique id of sample identifier to check the records in metadata tables
        unique_key_id = list(
            app_model.objects.filter(id=pk).values_list(
                unique_key["name"].lower(), flat=True
            )
        )[0]
        app_model.objects.filter(id=pk).delete()

        # Iterating through the metadata tables and delete the records where given project has been deleted.
        for i in metadata_tables:
            metadataname = f"{name.split('_')[0]}_{name.split('_')[1]}_{i}_metadata"
            metadats = self.context["view"].get_queryset()[metadataname.lower()]
            metadata_key = f"{unique_key['name']}_id".lower()
            if metadats.objects.filter(**{metadata_key: unique_key_id}).exists():
                metadats.objects.filter(**{metadata_key: unique_key_id}).delete()

        return value


class DeleteProjectView(generics.GenericAPIView):
    serializer_class = DeletePostSerializer
    permission_classes = (IsAuthenticated,)
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
            "message": "Sample deleted successfully",
        }
        response = Response(data, status=status.HTTP_200_OK)
        return response
