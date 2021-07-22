"""Notes Serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from notes.models import Note


class NotesModelSerializer(serializers.ModelSerializer):
    """Notes serializers."""
    
    def create(self, validated_data):
        """Create a note with given user."""
        return Note.objects.create(**validated_data)

    class Meta:
        model = Note
        fields = ['title', 'content']