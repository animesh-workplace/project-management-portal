from django.apps import apps
from rest_framework.response import Response
from schema_management.models import ProjectHandler
from rest_framework.permissions import IsAuthenticated
from user_management.api.utils import create_uniform_response
from rest_framework import generics, exceptions, serializers, status


class ProjectNamesSerializer(serializers.Serializer):
    class Meta:
        fields = "__all__"

    def validate(self, value):
        user = self.context["request"].user
        project_model = self.context["view"].get_queryset()
        # donot use single letter variables
        projects = [
            v
            for k, v in project_model.items()
            if k.startswith(user.username.lower()) and k.endswith("si")
        ]
        response = {}
        response["projects"] = [str(i).split(".")[2][0:-2] for i in projects]
        return response


class ProjectNamesView(generics.GenericAPIView):
    queryset = apps.get_app_config("table_factory").models
    serializer_class = ProjectNamesSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        if self.serializer.is_valid():
            return Response(self.serializer.validated_data)
        return Response(
            create_uniform_response(self.serializer.errors),
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )
