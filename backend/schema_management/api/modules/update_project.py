from django.apps import apps
from rest_framework.response import Response
from table_factory.api.tasks import UpdateData
from rest_framework import generics, serializers
from schema_management.models import ProjectHandler
from rest_framework.permissions import IsAuthenticated
from user_management.api.utils import create_uniform_response
from rest_framework import generics, exceptions, serializers, status


class UpdateProjectSerializer(serializers.Serializer):
    # rename id to something else id is a restricted keyword
    pk = serializers.IntegerField()
    data = serializers.JSONField()
    name = serializers.CharField()

    class Meta:
        fields = None

    def validate(self, value):
        modelname = value.get("name")
        pk = value.get("pk")
        data = value.get("data")
        app_model = self.context["view"].get_queryset()[modelname.lower()]
        config_data = list(
            ProjectHandler.objects.filter(table_name=modelname).values_list(
                "config", flat=True
            )
        )[0]
        colmns = []
        for i in config_data:
            colmns.append(i["name"])
        checks_matching = True
        pk_list = list(app_model.objects.values_list("id", flat=True))
        if pk not in pk_list:
            checks_matching = False
            raise exceptions.ValidationError(f"Primary key is not exists")
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
                # if i["unique"] == True:
                #     l = list(app_model.objects.values_list(i["id"], flat=True))
                #     if row[i["id"]] not in l:
                #         checks_matching = False
                #         raise exceptions.ValidationError(f"{i['id']} is not exists")
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
            self.update_table(modelname, data, app_model, pk)
            return value

    @staticmethod
    def update_table(name, data, app_model, pk):
        UpdateData(name, data, app_model, pk)


class UpdateProjectView(generics.CreateAPIView):
    queryset = apps.get_app_config("table_factory").models
    serializer_class = UpdateProjectSerializer
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
            "message": "Sample updated successfully",
        }
        response = Response(data, status=status.HTTP_200_OK)
        return response
