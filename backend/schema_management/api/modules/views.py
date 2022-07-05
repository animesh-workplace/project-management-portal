from django.apps import apps
from schema_management.models import ProjectHandler, MetadataHandler
from rest_framework.response import Response
from rest_framework import generics, serializers, viewsets
from table_factory.api.tasks import UploadProjectData
from rest_framework.permissions import IsAuthenticated
from user_management.api.utils import create_uniform_response
from rest_framework import generics, exceptions, serializers, status

app_models = apps.get_app_config("table_factory")


# class ProjectDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = None


# class ProjectDetailView(viewsets.ModelViewSet):
#     def get(self, request):
#         # app_model = app_models.models["root_icgc_si"]
#         queryset = app_models.models["root_icgc_si"].objects.all()
#         serializer = ProjectDetailSerializer(queryset, many=True)
#         print(serializer.data)
#         return Response({"data": serializer.data})


#     def get_queryset(self):
#         model = self.kwargs.get("root_icgc_si")
#         return model.objects.all()

#     def get_serializer_class(self):
#         ProjectDetailSerializer.Meta.model = self.kwargs.get("root_icgc_si")
#         return ProjectDetailSerializer


class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = None


class ProjectDetailView(viewsets.ModelViewSet):
    def get_queryset(self):
        model = self.kwargs.get(app_models.models["root_icgc_si"])
        return model.objects.all()

    def get_serializer_class(self):
        ProjectDetailSerializer.Meta.model = self.kwargs.get("model")
        return ProjectDetailSerializer
