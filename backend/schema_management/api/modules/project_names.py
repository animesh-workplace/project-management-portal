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
        project_names = (
            self.context["view"]
            .get_queryset()
            .objects.values_list("name", flat=True)
            .filter(table_name__startswith=user.username)
        )
        return project_names


class ProjectNamesView(generics.GenericAPIView):
    queryset = ProjectHandler
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectNamesSerializer

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        if self.serializer.is_valid():
            return Response({"projects": self.serializer.validated_data})
        return Response(
            create_uniform_response(self.serializer.errors),
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )
