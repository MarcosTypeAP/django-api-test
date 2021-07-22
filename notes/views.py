"""Notes Views."""

# Django REST Framework
from rest_framework import viewsets

# Permissions
from rest_framework.permissions import IsAuthenticated
from notes.permissions import IsNoteOwner

# Serializers
from notes.serializers import NotesModelSerializer

# Models
from notes.models import Note


class NotesAPIViewSet(viewsets.ModelViewSet):
    """Notes API view set."""

    queryset = Note.objects.all()
    serializer_class = NotesModelSerializer

    def perform_create(self, serializer):
        """Add the request user to the serializer."""
        serializer.save(user=self.request.user)

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions.append(IsNoteOwner)
        return [p() for p in permissions]