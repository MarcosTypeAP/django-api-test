"""Notes Models."""

# Django
from django.db import models

# Utils
from utils.models import NotesAPITest


class Note(NotesAPITest, models.Model):
    """Note model."""

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    content = models.TextField(max_length=500, blank=True)

    def __str__(self):
        """Return the title and user's username."""
        return f'{self.user.username}@{self.title}'
