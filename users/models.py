"""User Models"""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser

# Utils
from utils.models import NotesAPITest


class User(NotesAPITest , AbstractUser):
    """User model.
    
    User model that inherit of django's abstract user.
    Changes the username to email for authentication.
    """

    email = models.EmailField(unique=True)

    username = models.CharField(max_length=20, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'last_name', 'first_name']

    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)

    is_client = models.BooleanField(
        'client',
        default=True,
        help_text="Clients are the main class of users"
    )

    is_verified = models.BooleanField(
        'Verified',
        default=False,
        help_text="Sets true when the user verifies their account."
    )

    def __str__(self):
        """Return the username."""
        return self.username

    def get_short_name(self):
        """Return the username."""
        return self.username