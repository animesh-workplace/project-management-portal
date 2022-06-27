from django.db.models import Q
from user_management.models import MailToken
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import serializers, status, generics
from ..utils import create_uniform_response, OnlyUnAuthenticated


class ActivateSerializer(serializers.Serializer):
    """Activate Serializer: Validates the activation related parameters

    Parameters
    ----------
    username : string
            The username of the user <Required>
    token : string
            The token of the user <Required>
    email : string
            The email of the user <Required>

    Returns
    -------
    User Object
        Authenticated user object
    """
    token = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        fields = None

    def validate(self, value):
        email = value.get('email')
        token = value.get('token')
        username = value.get('username')

        user = self.get_user(username, email)
        if(not user):
            raise serializers.ValidationError({'Error': 'Invalid credentials'}, code='natural')
        self.validate_auth_user_status(user)
        self.validate_auth_user_token(user, token)
        user.is_active = True
        user.save()
        return user

    def get_user(self, username=None, email=None):
        user_obj = self.context['view'].get_queryset().objects.filter(
            Q(username__iexact=username) & Q(email__iexact=email)
        ).distinct()

        if(user_obj.exists()):
            user_obj = user_obj.first()
            return user_obj
        return None

    @staticmethod
    def validate_auth_user_status(user):
        if(user.is_active):
            raise serializers.ValidationError({'Error': 'User is already active'}, code='natural')

    @staticmethod
    def validate_auth_user_token(user, token):
        try:
            token_database = MailToken.objects.get(user=user, token_type=1)
            if(token_database.key == token):
                token_database.delete()
                return token
            raise serializers.ValidationError({'Error': 'Expired Token'}, code='natural')
        except MailToken.DoesNotExist:
            raise serializers.ValidationError({'Error': 'Invalid Token'}, code='natural')


class ActivateAPIView(generics.GenericAPIView):
    """Activate API: Activates the user to use the webapp

    Parameters
    ----------
    username : string
            The username of the user <Required>
    token : string
            The token of the user <Required>
    email : string
            The email of the user <Required>

    Returns
    -------
    Dict
            Dict containing 'message' and 'code' with success/failure
    """
    queryset = get_user_model()
    serializer_class = ActivateSerializer
    permission_classes = [OnlyUnAuthenticated]

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        if(self.serializer.is_valid()):
            return self.get_response()
        return Response(create_uniform_response(self.serializer.errors), status=status.HTTP_406_NOT_ACCEPTABLE)

    def get_response(self):
        data = {
            'code': 'SUCCESS',
            'message': 'Activation Successful',
        }
        response = Response(data, status=status.HTTP_200_OK)
        return response
