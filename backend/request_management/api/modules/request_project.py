from user_management.models import User
from rest_framework.response import Response
from request_management.models import UserRequest
from rest_framework.permissions import IsAuthenticated
from user_management.api.utils import create_uniform_response
from schema_management.models import MetadataHandler, ProjectHandler
from rest_framework import generics, exceptions, serializers, status


class UserRequestSerializer(serializers.Serializer):
    project = serializers.CharField()
    sop = serializers.CharField()

    class Meta:
        fields = None

    def validate_project(self, project):
        if ProjectHandler.objects.filter(name__iexact=project).exists():
            return project
        raise exceptions.ValidationError("Project doesn't exists")

    def validate(self, value):
        project = value.get("project")
        sop = value.get("sop")
        username = self.context["request"].user
        project_name = f"{username.username}_{project}_si"
        instance = self.context["view"].get_queryset().objects
        rejected_project = instance.values_list("projects_id", flat=True).filter(
            status="3", username=username
        )
        print(rejected_project)
        request_check = (
            instance.values("status")
            .filter(username=username, projects_id=project_name)
            .first()
        )
        self.check_requested_project(project, instance, request_check)
        self.check_accepted_project(project, username)
        self.check_rejected(project_name, rejected_project, instance, username, sop)
        self.upload_request(instance, username, project_name, sop)
        return value

    @staticmethod
    def check_requested_project(project, instance, request_check):
        if request_check == None:
            return
        if request_check["status"] == "1":
            raise exceptions.ValidationError(
                f"You have already requested for {project}. Please wait until your request processed"
            )

    @staticmethod
    def check_accepted_project(project, username):
        if project in list(username.projects):
            raise exceptions.ValidationError(
                f"You are already having access to {project}."
            )

    @staticmethod
    def check_rejected(project_name, rejected_project, instance, username, sop):
        if project_name in rejected_project:
            instance.filter(username=username).update(status="1", sop=sop)
            raise exceptions.ValidationError(f"Request updated successfully")

    @staticmethod
    def upload_request(instance, username, project_name, sop):
        instance.create(username=username, projects_id=project_name, sop=sop)


class UserRequestView(generics.CreateAPIView):
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
