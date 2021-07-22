"""User Serializers"""

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Django
from django.contrib.auth import authenticate, password_validation
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings

# Models
from users.models import User

# Utils
from datetime import timedelta
import jwt


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
        if not user.is_verified:
            raise serializers.ValidationError("Account is not active yet :(")
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
        user = User.objects.create_user(**data, is_verified=False)
        self.send_confirmation_email(user)
        return user

    def send_confirmation_email(self, user):
        """Send account verification link to given user."""
        token = self.generate_verification_token(user)
        subject = f'Welcome @{user.username}. Verify your account to start using this API.'
        from_email = 'API Test <noreply@apitest.com>'
        content = render_to_string(
            template_name='emails/users/account_verification.html',
            context={'token': token, 'user': user}
        )
        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        msg.attach_alternative(content, 'text/html')
        msg.send()

    def generate_verification_token(self, user):
        """Generate a JWT that the user can use to verify their account."""
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'user': user.username,
            'exp': int(exp_date.timestamp()),
            'type': 'email_confirmation',
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token


class AccountVerificationSerializer(serializers.Serializer):
    """User's account verification serializer."""

    token = serializers.CharField()

    def validate_token(self, data):
        """Verify token is valid."""
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired.')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token.')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid token.')
        
        self.context['payload'] = payload
        return data

    def save(self):
        """Update user's verified status."""
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()