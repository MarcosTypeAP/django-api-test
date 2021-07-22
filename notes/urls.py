"""Notes URLs."""

# Django REST Framework
from django.contrib.admin.decorators import action
from rest_framework.routers import DefaultRouter

# Django
from django.urls import path, include

# Views
from notes.views import NotesAPIViewSet


router = DefaultRouter()
router.register(r'', NotesAPIViewSet, basename='notes')

urlpatterns = [

    path('', include(router.urls))

]