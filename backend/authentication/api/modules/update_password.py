from ..utils import create_uniform_response
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, status, generics


class UpdatePasswordSerializer(serializers.Serializer):
    """Cookie Refresh Serializer: Extracts the refresh cookie token from the user request

    Parameters
    ----------
    jwt-refresh : Cookie
            The cookie containing the refresh token

    Returns
    -------
    String
        Refresh token
    """
    old_password = serializers.CharField(required=True, style={'input_type': 'password'}, write_only=True)
    new_password = serializers.CharField(required=True, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = None
        extra_kwargs = {'old_password': {'write_only': True}, 'new_password': {'write_only': True}}

    def validate(self, value):
        new_password = value.get('new_password')
        old_password = value.get('old_password')
        if(old_password == new_password):
            raise serializers.ValidationError({'Error': 'Both password are identical'}, code='natural')
        instance = self.context['request'].user
        if(instance.check_password(old_password)):
            instance.set_password(new_password)
            instance.save()
            return value
        raise serializers.ValidationError({'Error': 'Invalid Password'}, code='natural')


class UpdatePasswordView(generics.GenericAPIView):
    """Authentication Status API: Send the user authentication status

    Parameters
    ----------
    jwt-auth : Cookie
            The cookie containing the auth token
    jwt-refresh : Cookie
            The cookie containing the refresh token

    Returns
    -------
    String
        Authentication status:
            - Refreshable
            - Authenticated
            - Unauthenticated
    """
    serializer_class = UpdatePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        if(self.serializer.is_valid()):
            return Response({
                'code': 'SUCCESS',
                'message': 'Password Updated Successfully',
            })
        return Response(create_uniform_response(self.serializer.errors), status=status.HTTP_406_NOT_ACCEPTABLE)
