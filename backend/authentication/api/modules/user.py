from rest_framework.utils import model_meta
from ..utils import create_uniform_response
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, generics, status
from rest_framework.serializers import raise_errors_on_nested_writes


class UserDetailSerializer(serializers.Serializer):
    """User Detail Serializer: Fetches the user related information and updates the data

    Parameters
    ----------
    bio : string
            The bio of the user <Required if updating in PUT>
    avatar : string
            The avatar of the user <Required if updating in PUT>
    poster : string
            The poster of the user <Required if updating in PUT>
    last_name : string
            The last_name of the user <Required if updating in PUT>
    first_name : string
            The first_name of the user <Required if updating in PUT>
    birth_date : string
            The birth date of the user <Required if updating in PUT>
    city : string
            The city of the user <Required if updating in PUT>
    state : string
            The state of the user <Required if updating in PUT>
    address : string
            The address of the user <Required if updating in PUT>
    institute : string
            The institute of the user <Required if updating in PUT>
    job_profile : string
            The job_profile of the user <Required if updating in PUT>
    pin_code : string
            The pin_code of the user <Required if updating in PUT>

    Returns
    -------
    POST:
            User Dict
                    Authenticated user object in the form of dict with field values
    PUT:
            Success/Failure message
    """

    bio = serializers.CharField(required=False)
    avatar = serializers.ImageField(required=False)
    poster = serializers.ImageField(required=False)
    last_name = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    birth_date = serializers.DateField(required=False)
    city = serializers.CharField(required=False, max_length=255)
    state = serializers.CharField(required=False, max_length=255)
    address = serializers.CharField(required=False, max_length=1000)
    institute = serializers.CharField(required=False, max_length=500)
    job_profile = serializers.CharField(required=False, max_length=255)
    pin_code = serializers.DecimalField(required=False, max_digits=10, decimal_places=0)

    class Meta:
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "city",
            "state",
            "avatar",
            "poster",
            "address",
            "pin_code",
            "institute",
            "birth_date",
            "job_profile",
            "user_type",
            "login_history",
            "date_joined",
        ]
        model = get_user_model()

    def validate(self, value):
        if self.context["request"].META["REQUEST_METHOD"] == "POST":
            user = self.context["request"].user
            value = {
                attr: getattr(user, attr, None)
                if (attr not in ["avatar", "poster"])
                else getattr(user, attr, None).url
                for attr in self.Meta.fields
            }
            return {
                "data": value,
                "code": "SUCCESS",
                "message": "User information",
            }
        elif self.context["request"].META["REQUEST_METHOD"] == "PUT":
            return value

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes("update", self, validated_data)
        info = model_meta.get_field_info(instance)

        m2m_fields = []
        for (attr, value) in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)
        instance.save()

        for (attr, value) in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)
        return instance


class UserDetailView(generics.GenericAPIView):
    """UserDetailView API: Sends authenticated user information and updates those information

    Parameters
    ----------
    jwt-auth : Cookie
            Cookie received after authenticating and used to get authenticated pages and data
    jwt-refresh : Cookie
            Cookie received after authenticating and used to get new auth token
    csrf_token : Cookie
            Cookie used to verify the Request source is same

    Methods
    ----------
    POST, PUT

    Returns
    -------
    POST:
            User information: dict
    PUT:
            Message
    """

    queryset = get_user_model()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        if self.serializer.is_valid():
            return Response(self.serializer.validated_data)
        return Response(
            create_uniform_response(self.serializer.errors),
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )

    def put(self, request, *args, **kwargs):
        user_obj = request.user
        self.serializer = self.get_serializer(data=request.data)
        if self.serializer.is_valid():
            validated_data = self.serializer.validated_data
            if bool(validated_data):
                self.serializer.update(user_obj, validated_data)
                return Response(
                    {
                        "code": "SUCCESS",
                        "message": "Updated Successfully",
                    }
                )
            return Response({"message": "No data updated"})
        return Response(
            create_uniform_response(self.serializer.errors),
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )
