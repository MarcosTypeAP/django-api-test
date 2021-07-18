"""Users Views"""

# Django REST Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Serializers
from users.serializers import (
    UserLoginSerializer,
    UserSerializer,
    UserSignUpSerializer,
)


class UserLoginView(APIView):
    """User login view"""

    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserSerializer(user).data,
            'access_token': token,
        }
        return Response(data, status=status.HTTP_201_CREATED)


class UserSignUpView(APIView):
    """User sign up view"""

    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)
