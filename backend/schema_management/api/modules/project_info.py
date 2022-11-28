from django.apps import apps
from rest_framework.response import Response
from schema_management.models import ProjectHandler
from rest_framework.permissions import IsAuthenticated
from user_management.api.utils import create_uniform_response
from rest_framework import generics, exceptions, serializers, status


class ProjectDetailSerializer(serializers.Serializer):
    name = serializers.CharField()

    class Meta:
        fields = "__all__"

    def validate(self, value):
        name = value.get("name")
        if ProjectHandler.objects.filter(table_name__iexact=name).exists():
            project_model = self.context["view"].get_queryset()[name.lower()]
            queryset = project_model.objects.all().values()
            return queryset

        raise exceptions.ValidationError(f"{name} is not exists in metadata_model")


class ProjectDetailView(generics.GenericAPIView):
    queryset = apps.get_app_config("table_factory").models
    serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        if self.serializer.is_valid():
            return Response(self.serializer.validated_data)
        return Response(
            create_uniform_response(self.serializer.errors),
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )
