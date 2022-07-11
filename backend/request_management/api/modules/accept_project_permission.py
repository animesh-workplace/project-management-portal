from user_management.models import User
from rest_framework.response import Response
from request_management.models import UserRequest
from rest_framework.permissions import IsAuthenticated
from user_management.api.utils import create_uniform_response
from schema_management.models import MetadataHandler, ProjectHandler
from rest_framework import generics, exceptions, serializers, status


class ProjectPermissionsSerializer(serializers.Serializer):
    pass
