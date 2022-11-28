from django.apps import apps
from rest_framework.response import Response
from table_factory.api.tasks import UpdateData
from rest_framework import generics, serializers
from schema_management.models import MetadataHandler
from rest_framework.permissions import IsAuthenticated
from user_management.api.utils import create_uniform_response
from rest_framework import generics, exceptions, serializers, status


class UpdateMetadataSerializer(serializers.Serializer):
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
        split_modelname = modelname.split("_")
        project_name = f"{split_modelname[0]}_{split_modelname[1]}_si"
        project_model = self.context["view"].get_queryset()[project_name.lower()]

        print(project_model)
        config_data = list(
            MetadataHandler.objects.filter(table_name__iexact=modelname).values_list(
                "config", flat=True
            )
        )[0]

        project_unique_field = (
            config_data[0]["name"].replace(config_data[0]["name"][-3:], "").lower()
        )
        project_unique_values = list(
            project_model.objects.values_list(project_unique_field, flat=True)
        )
        print(project_unique_values)
        print(config_data[0]["name"].replace(config_data[0]["name"][-3:], ""))
        print(app_model)
        colmns = []
        for i in config_data:
            colmns.append(i["name"].lower())
        checks_matching = True
        pk_value = (app_model.objects.values("id").filter(id=pk))[0]
        pk_list = app_model.objects.values_list("id", flat=True)
        if pk_value["id"] not in pk_list:
            checks_matching = False
            raise exceptions.ValidationError(f"{pk} is not exists")
        for row in data:
            for i in config_data:
                if not i["name"].lower() in row:
                    checks_matching = False
                    raise exceptions.ValidationError(
                        f"{app_model} requires column {i['name'].lower()}"
                    )
                for col in row.keys():
                    if not col in colmns:
                        checks_matching = False
                        raise exceptions.ValidationError(
                            f"{app_model} doesn't have column {col}"
                        )
                # print(col)
                if i["unique"] == True:
                    l = list(
                        app_model.objects.values_list(i["name"].lower(), flat=True)
                    )
                    print(l)
                    l1 = list(
                        app_model.objects.values_list(
                            i["name"].lower(), flat=True
                        ).filter(id=pk)
                    )[0]
                    l.remove(l1)

                    if row[i["name"].lower()] in l:
                        checks_matching = False
                        raise exceptions.ValidationError(
                            f"{i['name'].lower()} with value '{row[i['name'].lower()]}' exists in '{modelname.replace('_', ' ')}'"
                        )
                    if row[i["name"].lower()] not in project_unique_values:
                        checks_matching = False
                        raise exceptions.ValidationError(
                            f"{i['name'].lower()} with value '{row[i['name'].lower()]}' not exists in '{project_name.replace('_', ' ')}'"
                        )
                if "options" in i and i["data_type"] == "radio":
                    if not row[i["name"].lower()] in i["options"]:
                        checks_matching = False
                        raise exceptions.ValidationError(
                            f"Select {i['name'].lower()} from any one of {i['options']} only. Eg. '{i['name'].lower()}': '{i['options'][0]}'"
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


class UpdateMetadataView(generics.CreateAPIView):
    queryset = apps.get_app_config("table_factory").models
    serializer_class = UpdateMetadataSerializer
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
