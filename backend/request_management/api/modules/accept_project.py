import datetime
from user_management.models import User
from rest_framework.response import Response
from request_management.models import UserRequest
from rest_framework.permissions import IsAuthenticated
from user_management.api.utils import create_uniform_response
from rest_framework import generics, exceptions, serializers, status


class ProjectPermissionsSerializer(serializers.Serializer):
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
        existed_projects.append(project)
        user_id = User.objects.filter(username__iexact=username).values("id").first()
        requested_project = instance.values_list("projects_id", flat=True).filter(
            status="1", username=user_id["id"]
        )
        if user.user_type == 2:
            self.check_project(user, project, requested_project)
            self.accpet_project(
                instance, username, existed_projects, status, user_id, comments
            )
            return value
        raise exceptions.ValidationError("Only project admin has this permissions")

    @staticmethod
    def check_project(user, project, requested_project):
        if not f"{user.username}_{project}_si" in requested_project:
            raise exceptions.ValidationError("Please provide requested project only")

    @staticmethod
    def accpet_project(instance, username, existed_projects, status, user_id, comments):
        User.objects.filter(username__iexact=username).update(projects=existed_projects)
        instance.filter(username=user_id["id"]).update(
            status=status, comments=comments, response_time=datetime.datetime.now()
        )


class ProjectPermissionsView(generics.GenericAPIView):
    queryset = UserRequest
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectPermissionsSerializer

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
