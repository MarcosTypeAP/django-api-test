"""User Serializers"""

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Django
from django.contrib.auth import authenticate, password_validation

# Models
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """User serializer.
    
    Display the username, email, first name and last name.
    """

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class UserLoginSerializer(serializers.Serializer):
    """User login serializer.
    
    Handle the login request data.
    """

    email = serializers.EmailField()

    password = serializers.CharField()

    def validate(self, data):
        """Check credentials."""
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        self.context['user'] = user
        return data

    def create(self, data):
        """Create or retrive a new token."""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class UserSignUpSerializer(serializers.Serializer):
    """User sign up serializer.
    
    Handle the sign up request data.
    """

    email = serializers.EmailField(
        validators = [
            UniqueValidator(queryset=User.objects.all()),
        ]
    )

    username = serializers.CharField(
        min_length=4, 
        max_length=20, 
        validators = [
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    first_name = serializers.CharField(min_length=2, max_length=40)
    last_name = serializers.CharField(min_length=2, max_length=40)

    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check if passwords match."""
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Passwords don't match.")
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        """Handle user creation."""
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        return user