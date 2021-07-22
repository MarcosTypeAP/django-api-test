"""Notes Permission classes."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from notes.models import Note


class IsNoteOwner(BasePermission):
    """Allow modify only the note owner."""
    
    def has_object_permission(self, request, view, obj):
        """Verify the user is the note owner."""
        if obj.user != request.user:
            return False
        return True