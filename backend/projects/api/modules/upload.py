from django.apps import apps
from projects.models import Projectname
from rest_framework.response import Response
from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated

app_models = apps.get_app_config("projects")


class UploadSerializer(serializers.Serializer):
    data = serializers.JSONField()
    name = serializers.CharField()

    class Meta:
        fields = None

    def validate(self, value):
        name = value.get("name")
        data = value.get("data")

        model_name = f"{name.lower()}_sample_identifier"
        model_schema = self.create_model(model_name)
        self.create_model_fields(model_schema, config)
        Projectname.objects.create(modelname=model_name, config_file=config)
        self.register_model(model_schema)
        return value


class UploadView(generics.CreateAPIView):
    queryset = apps.get_app_config("projects")
    serializer_class = UploadSerializer
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

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        modelname = serializer.validated_data["modelname"]
        data = serializer.validated_data["data"]
        app_model = app_models.models[modelname.lower()]
        config_data = Projectname.objects.filter(modelname=modelname).values_list(
            "config_file", flat=True
        )
        print(config_data)
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
                        {"message": f"{app_model} requires column {i['field']}"}
                    )
                for col in row.keys():
                    if not col in colmns:
                        checks_matching = False
                        return Response(
                            {"message": f"{app_model} doesn't have column {col}"}
                        )
                if i["unique"] == True:
                    l = list(app_model.objects.values_list(i["field"], flat=True))
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
            obj_list = [app_model(**data_dict) for data_dict in data]
        app_model.objects.bulk_create(obj_list)
        return Response({"message": "Data uploaded successfully"})
