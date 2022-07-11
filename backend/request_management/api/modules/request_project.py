from user_management.models import User
from rest_framework.response import Response
from request_management.models import UserRequest
from rest_framework.permissions import IsAuthenticated
from user_management.api.utils import create_uniform_response
from schema_management.models import MetadataHandler, ProjectHandler
from rest_framework import generics, exceptions, serializers, status


class UserRequestSerializer(serializers.Serializer):
    requested_project = serializers.CharField()

    class Meta:
        fields = None

    def validate(self, value):
        requested_project = value.get("requested_project")
        username = self.context["request"].user
        project_name = f"{username.username}_{requested_project}_si"
        queryset = self.context["view"].get_queryset().objects
        projects_list = list(ProjectHandler.objects.values_list("name", flat=True))
        rejected_project = queryset.values_list(
            "requested_projects_id", flat=True
        ).filter(request_status="3", username=username)

        if project_name in rejected_project:
            queryset.filter(username=username).update(
                request_status="1",
            )
            return value
        if not requested_project in projects_list:
            raise exceptions.ValidationError(
                f"Please select project name from {projects_list} only."
            )
        if queryset.filter(username=username).first() is None:
            queryset.create(username=username, requested_projects_id=project_name)
            return value

        if requested_project in list(username.projects):
            raise exceptions.ValidationError(
                f"You are already having access to {requested_project}."
            )
        request_check = (
            queryset.values("request_status")
            .filter(username=username, requested_projects_id=project_name)
            .first()
        )
        if request_check == None:
            queryset.create(username=username, requested_projects_id=project_name)
            return value
        if request_check["request_status"] == "1":
            raise exceptions.ValidationError(
                f"You have already requested for {requested_project}. Please wait until your request processed"
            )
        queryset.create(username=username, requested_projects_id=project_name)
        return value


class UserRequestApi(generics.CreateAPIView):
    queryset = UserRequest
    permission_classes = [IsAuthenticated]
    serializer_class = UserRequestSerializer

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
            "message": "Request submitted successfully",
        }
        response = Response(data, status=status.HTTP_200_OK)
        return response
