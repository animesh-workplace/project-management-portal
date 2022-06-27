import os
from dotenv import load_dotenv
from django.conf import settings
from ..tasks import send_email_activate
from user_management.models import MailToken
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from ..utils import create_uniform_response, OnlyUnAuthenticated
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import serializers, status, generics, exceptions

load_dotenv(settings.BASE_DIR / '.env')


class RegisterSerializer(serializers.Serializer):
    """Register Serializer: Validates the user entered parameters and
    creates a new user in the database

        Parameters
        ----------
        username : string
                The username of the user
        password : string
                The password of the user
        password2 : string
                The confirmation password of the user
        email : string
                The email of the user
        last_name : string
                The last name of the user
        first_name : string
                The first name of the user

        Returns
        -------
        User Object
                Registered user object
        """
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = None
        extra_kwargs = {'password': {'write_only': True}}

    @method_decorator(sensitive_post_parameters('password', 'password2'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def validate_username(self, username):
        qs = self.context['view'].get_queryset().objects
        if (qs.filter(username__iexact=username).exists()):
            raise exceptions.ValidationError('Already exists')
        return username

    def validate_email(self, email):
        qs = self.context['view'].get_queryset().objects
        if (qs.filter(email__iexact=email).exists()):
            raise exceptions.ValidationError('Already exists')
        return email

    def validate(self, value):
        pw1 = value.get('password')
        pw2 = value.pop('password2')
        if (pw1 != pw2):
            raise exceptions.ValidationError('Passwords must match')
        return value

    def create(self, validated_data):
        instance = self.context['view'].get_queryset()(**validated_data)
        instance.set_password(validated_data.get('password'))
        instance.is_active = False
        instance.save()
        token = MailToken.objects.create(user=instance, token_type=1)
        activation_link = (f"{os.getenv('BASE_LINK')}{os.getenv('BASE_URL')}auth/activation?username={instance.username}"
                           f"&email={instance.email}&token={token}")
        send_email_activate(instance.first_name, instance.username, instance.email, activation_link)
        return instance


class RegisterView(generics.CreateAPIView):
    """Register API: Creates a new user in the database

        Parameters
        ----------
        username : string
                The username of the user
        password : string
                The password of the user
        password2 : string
                The confirmation password of the user
        email : string
                The email of the user
        last_name : string
                The last name of the user
        first_name : string
                The first name of the user

        Returns
        -------
        Dict
                Dict containing 'message' and 'code' with success/failure
        """
    queryset = get_user_model()
    serializer_class = RegisterSerializer
    permission_classes = [OnlyUnAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response({
                'message': 'Registered Successfully, check mail',
                'code': 'SUCCESS'
            })
        return Response(create_uniform_response(serializer.errors), status=status.HTTP_406_NOT_ACCEPTABLE)
