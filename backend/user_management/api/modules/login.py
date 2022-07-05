from django.db.models import Q
from ipware import get_client_ip
from django.conf import settings
from django.utils import timezone
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .jwt_utils import set_jwt_cookies, jwt_encode
from django.utils.decorators import method_decorator
from rest_framework import serializers, status, generics
from ..utils import create_uniform_response, OnlyUnAuthenticated
from django.views.decorators.debug import sensitive_post_parameters


class LoginSerializer(serializers.Serializer):
    """Login Serializer: Validates the user provided parameters

    Parameters
    ----------
    username : string
            The username of the user <Either of these params must be present>
    password : string
            The password of the user <Required>
    email : string
            The email of the user <Either of these params must be present>

    Returns
    -------
    User Object
        Authenticated user object
    """

    email = serializers.EmailField(required=False, allow_blank=True)
    username = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(style={"input_type": "password"})

    class Meta:
        fields = None
        extra_kwargs = {"password": {"write_only": True}}

    @method_decorator(sensitive_post_parameters("password"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def validate(self, value):
        email = value.get("email")
        username = value.get("username")
        password = value.get("password")

        user = self.validate_username_email(username, email, password)
        if not user:
            raise serializers.ValidationError(
                {"Error": "Invalid credentials"}, code="natural"
            )
        self.validate_auth_user_status(user)
        value["user"] = user
        return value

    def validate_username_email(self, username, email, password):
        if email and password:
            user = self.authenticate(email=email, password=password)
        elif username and password:
            user = self.authenticate(username=username, password=password)
        else:
            raise serializers.ValidationError(
                {"Error": "Must include either username or email"}, code="natural"
            )
        return user

    def authenticate(self, username=None, password=None, email=None):
        user_obj = (
            self.context["view"]
            .get_queryset()
            .objects.filter(Q(username__iexact=username) | Q(email__iexact=email))
            .distinct()
        )

        if user_obj.exists():
            user_obj = user_obj.first()
            if user_obj.check_password(password):
                return user_obj
        return None

    @staticmethod
    def validate_auth_user_status(user):
        if not user.is_active:
            raise serializers.ValidationError(
                {"Error": "User inactive"}, code="natural"
            )


class LoginView(generics.GenericAPIView):
    """Login API: Sends authenticated cookie back to the user

    Parameters
    ----------
    username : string
            The username of the user <Either of these params must be present>
    password : string
            The password of the user <Required>
    email : string
            The email of the user <Either of these params must be present>

    Returns
    -------
    Cookies
        Authenticated cookies jwt-auth, jwt-refresh and csrf_token
    Token
            CSRF token
    """

    queryset = get_user_model()
    serializer_class = LoginSerializer
    permission_classes = [OnlyUnAuthenticated]

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        if self.serializer.is_valid():
            self.login()
            return self.get_response()
        return Response(
            create_uniform_response(self.serializer.errors),
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )

    def login(self):
        user = self.serializer.validated_data["user"]
        client_ip, routable = get_client_ip(self.request)
        login_time = timezone.localtime(timezone.now())
        user.last_login = login_time
        user.login_history.append(
            {
                "IP": client_ip,
                "time": str(login_time),
            }
        )
        user.save()
        self.access_token, self.refresh_token, self.csrf_token = jwt_encode(user)

    def get_response(self):
        data = {
            "code": "SUCCESS",
            "message": "Logged in Successfully",
            "expiration": (
                timezone.localtime(timezone.now()) + settings.JWT_AUTH_LIFETIME
            ),
        }
        response = Response(data, status=status.HTTP_200_OK)
        set_jwt_cookies(
            response, self.access_token, self.refresh_token, self.csrf_token
        )
        return response
