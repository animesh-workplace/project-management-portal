from django.apps import apps
from rest_framework.response import Response
from schema_management.models import MetadataHandler
from rest_framework.permissions import IsAuthenticated
from user_management.api.utils import create_uniform_response
from rest_framework import generics, exceptions, serializers, status


class DeletePostSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

    class Meta:
        fields = "__all__"

    def validate(self, value):
        id = value.get("id")
        name = value.get("name")
        if not name in list(
            MetadataHandler.objects.values_list("table_name", flat=True).filter(
                table_name=name
            )
        ):
            raise exceptions.ValidationError("Project is not exists")
        app_model = self.context["view"].get_queryset()[name.lower()]
        l = list(app_model.objects.values_list("id", flat=True))
        if id not in l:
            raise exceptions.ValidationError("Id is not exists")
        app_model.objects.filter(id=id).delete()
        return value


class DeleteMeatadataView(generics.GenericAPIView):
    serializer_class = DeletePostSerializer
    permission_classes = (IsAuthenticated,)
    queryset = apps.get_app_config("table_factory").models

    def delete(self, request, *args, **kwargs):
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
