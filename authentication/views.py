from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import request, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import list_route
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from authentication.serializers import AuthenticationSerializer
from users.models import User
from users.serializers import UserSerializer


class AuthenticationViewSet(GenericViewSet):
    serializer_class = AuthenticationSerializer
    permission_classes = (AllowAny,)

    @list_route(methods=['POST'])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)

        if user:
            if not user.is_active:
                msg = 'User account is disabled.'
                raise ValidationError(msg, code='authorization')
        else:
            msg = 'Unable to log in with provided credentials.'
            raise ValidationError(msg, code='authorization')
        token = self.perform_login(request, user)
        return Response({'token': token.key})

    @list_route(methods=['POST'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_serializer = UserSerializer(data=serializer.validated_data)
        user_serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(**user_serializer.validated_data)
        token = self.perform_login(request, user)
        return Response({'token': token.key})

    @staticmethod
    def perform_login(request, user):
        token, created = Token.objects.get_or_create(user=user)
        django_login(request, user)
        return token

    @list_route(methods=['POST'])
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        django_logout(request)
        return Response('Logged out', status=status.HTTP_200_OK)
