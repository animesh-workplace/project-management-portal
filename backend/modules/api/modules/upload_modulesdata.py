from django.apps import apps
from rest_framework import generics
from modules.models import Modulename
from rest_framework import serializers
from projects.models import Projectname
from modules.models import Modulename
from rest_framework.response import Response

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from projects.models import *

app_models = apps.get_app_config("projects")


class GetModuledata(generics.ListAPIView):
    def get(self, request):
        projects = self.request.GET.get("projects")
        a = app_models.models
        modules = [
            v
            for k, v in a.items()
            if k.startswith(projects.lower()) and k.endswith("module")
        ]
        response = {}
        for i in modules:
            queryset = i.objects.all().values()
            response[str(i).split(".")[2][0:-2]] = queryset
        return Response(response)


class PostdataSerializer1(serializers.Serializer):
    modulename = serializers.CharField()
    data = serializers.ListField()


class CreateModuledata(generics.CreateAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = PostdataSerializer1

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        modulename = serializer.validated_data["modulename"]
        data = serializer.validated_data["data"]
        app_module = app_models.models[modulename.lower()]
        config_data = Modulename.objects.filter(modulename=modulename).values_list(
            "config_file", flat=True
        )
        # Getting config file
        config_file = []
        for i in config_data:
            config_file = i
        # Pushing backend names of cilumns into list
        colmns = []
        for i in config_file:
            colmns.append(i["field"])
        checks_matching = True
        for row in data:
            for i in config_file:
                if not i["field"] in row:
                    checks_matching = False
                    return Response(
                        {"message": f"{app_module} requires column {i['field']}"}
                    )
                for col in row.keys():
                    if not col in colmns:
                        checks_matching = False
                        return Response(
                            {"message": f"{app_module} doesn't have column {col}"}
                        )
                if i["unique"] == True:
                    l = list(app_module.objects.values_list(i["field"], flat=True))
                    if row[i["field"]] in l:
                        checks_matching = False
                        return Response({"message": f"{i['field']} is exists"})
                if "options" in i and i["datatype"] == "radio":
                    if not row[i["field"]] in i["options"]:
                        checks_matching = False
                        return Response(
                            {
                                "message": f"Select {i['field']} from any one of {i['options']} only. Eg. '{i['field']}': '{i['options'][0]}'"
                            }
                        )
                if "options" in i and i["datatype"] == "multi radio":
                    for j in row[i["field"]]:
                        if not j in i["options"]:
                            checks_matching = False
                            return Response(
                                {
                                    "message": f"Select {i['field']} from choices of {i['options']} only. Eg. '{i['field']}': {i['options'][0:2]}"
                                }
                            )
        if checks_matching == True:
            obj_list = [app_module(**data_dict) for data_dict in data]
        app_module.objects.bulk_create(obj_list)
        return Response({"message": "Data uploaded successfully"})
