from django.apps import apps
from schema_management.models import ProjectHandler, MetadataHandler
from rest_framework.response import Response
from rest_framework import generics, serializers
from table_factory.api.tasks import UploadProjectData
from rest_framework.permissions import IsAuthenticated
from user_management.api.utils import create_uniform_response
from rest_framework import generics, exceptions, serializers, status


class UploadMetadataSerializer(serializers.Serializer):
    data = serializers.JSONField()
    name = serializers.CharField()

    class Meta:
        names = None

    def validate(self, value):
        modelname = value.get("name")
        data = value.get("data")
        app_model = self.context["view"].get_queryset()[modelname.lower()]
        config_data = list(
            MetadataHandler.objects.filter(table_name=modelname).values_list(
                "config", flat=True
            )
        )[0]
        colmns = []
        for i in config_data:
            colmns.append(i["name"])
        checks_matching = True
        for row in data:
            for i in config_data:
                if not i["name"] in row:
                    checks_matching = False
                    raise exceptions.ValidationError(
                        f"{app_model} requires column {i['name']}"
                    )
                for col in row.keys():
                    if not col in colmns:
                        checks_matching = False
                        raise exceptions.ValidationError(
                            f"{app_model} doesn't have column {col}"
                        )
                if i["unique"] == True:
                    l = list(app_model.objects.values_list(i["name"], flat=True))
                    if row[i["name"]] in l:
                        checks_matching = False
                        raise exceptions.ValidationError(f"{i['name']} is exists")
                if "options" in i and i["data_type"] == "radio":
                    if not row[i["name"]] in i["options"]:
                        checks_matching = False
                        raise exceptions.ValidationError(
                            f"Select {i['name']} from any one of {i['options']} only. Eg. '{i['name']}': '{i['options'][0]}'"
                        )
                if "options" in i and i["data_type"] == "multiradio":
                    for j in row[i["name"]]:
                        if not j in i["options"]:
                            checks_matching = False
                            raise exceptions.ValidationError(
                                f"Select {i['name']} from choices of {i['options']} only. Eg. '{i['name']}': {i['options'][0:2]}"
                            )
        if checks_matching == True:
            self.create_table(modelname, data, app_model)
            return value

    @staticmethod
    def create_table(name, data, app_model):
        UploadProjectData(name, data, app_model)


class UploadMetadataView(generics.CreateAPIView):
    queryset = apps.get_app_config("table_factory").models
    serializer_class = UploadMetadataSerializer
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
            "message": "Sample added successfully",
        }
        response = Response(data, status=status.HTTP_200_OK)
        return response
