"""NotesAPITest Utils"""

# Django
from django.db import models


class NotesAPITest(models.Model):
    """NotesAPITest base model.

    This model acts as a base model which every
    other models in the project will inherit.
    This class provides the following attributes:
        + created (DateTime): Stores the datetime the object was created.    
        + modified (DateTime): Stores the last datetime the object was modified.    
    """

    created = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text="Date and Time the object was created"
    )

    modified = models.DateTimeField(
        'modified at',
        auto_now=True,
        help_text="Date and Time the object was modified"
    )

    class Meta:
        """Meta options"""
        abstract = True

        get_latest_by = 'created'
        ordering = ['-created', '-modified']