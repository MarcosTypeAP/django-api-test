"""Notes Admin."""

# Django
from django.contrib import admin

# Models
from notes.models import Note


admin.site.register(Note)