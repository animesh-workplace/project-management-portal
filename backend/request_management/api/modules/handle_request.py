import datetime
from user_management.models import User
from rest_framework.response import Response
from request_management.models import UserRequest
from schema_management.models import ProjectHandler
from rest_framework.permissions import IsAuthenticated
from user_management.api.utils import create_uniform_response
from rest_framework import generics, exceptions, serializers, status


class HandleRequestSerializer(serializers.Serializer):
    """Handle Request Serializer: Validates the request handling related parameters

    Parameters
    ----------
    username : string
            The username of the user <Required>
    project : string
            The project which permissions are accepting or denying <Required>
    status : string
            The email project <Required>
    comments : text
            Comments on handled project permissions <Required>

    Returns
    -------
    Ordered dictionary of validated data
    """

    username = serializers.CharField()
    project = serializers.CharField()
    status = serializers.CharField()
    comments = serializers.CharField()

    class Meta:
        fields = None

    def validate_username(self, username):
        if User.objects.filter(username__iexact=username).exists():
            return username
        raise exceptions.ValidationError("User doesn't exists")

    def validate_project(self, project):
        if ProjectHandler.objects.filter(name__iexact=project).exists():
            return project
        raise exceptions.ValidationError("Project doesn't exists")

    def validate_status(self, status):
        if not status in ["1", "2", "3"]:
            raise exceptions.ValidationError("Please select valid status")
        if status == "1":
            raise exceptions.ValidationError("Status is already in requested mode")
        return status

    def validate(self, value):
        username = value.get("username")
        project = value.get("project")
        status = value.get("status")
        comments = value.get("comments")
        user = self.context["request"].user
        instance = self.context["view"].get_queryset().objects
        existed_projects = list(
            User.objects.filter(username__iexact=username)
            .values_list("projects", flat=True)
            .first()
        )
        project_id = f"{user.username}_{project}_si"
        existed_projects.append(project)
        user_id = User.objects.filter(username__iexact=username).values("id").first()
        requested_project = instance.values_list("projects_id", flat=True).filter(
            status="1", username=user_id["id"]
        )
        self.check_project(user, project, requested_project)
        self.handle_request(
            instance,
            username,
            existed_projects,
            status,
            user_id,
            comments,
            project_id,
        )
        print(value)
        return value

    @staticmethod
    def check_project(user, project, requested_project):
        if not f"{user.username}_{project}_si" in requested_project:
            raise exceptions.ValidationError("Please provide requested project only")

    @staticmethod
    def handle_request(
        instance, username, existed_projects, status, user_id, comments, project_id
    ):
        if status == "3":
            instance.filter(username=user_id["id"], projects_id=project_id).update(
                status=status, comments=comments, response_time=datetime.datetime.now()
            )
            raise exceptions.ValidationError("Project permissions are rejected.")
        User.objects.filter(username__iexact=username).update(projects=existed_projects)
        instance.filter(username=user_id["id"], projects_id=project_id).update(
            status=status, comments=comments, response_time=datetime.datetime.now()
        )


class HandleRequestView(generics.GenericAPIView):
    """Handle Request API: Handles the user request to the project

    Parameters
    ----------
    username : string
            The username of the user <Required>
    project : string
            The project which permissions are accepting or denying <Required>
    status : string
            The email project <Required>
    comments : text
            Comments on handled project permissions <Required>

    Returns
    -------
    Dict
            Dict containing 'message' and 'code' with success/failure
    """

    queryset = UserRequest
    permission_classes = [IsAuthenticated]
    serializer_class = HandleRequestSerializer

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
            "message": "Acceptation done successfully",
        }
        response = Response(data, status=status.HTTP_200_OK)
        return response
