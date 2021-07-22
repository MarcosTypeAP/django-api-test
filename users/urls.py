"""Users URLs"""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from users import views as user_views


router = DefaultRouter()
router.register(r'', user_views.UserViewSet, basename='users')

urlpatterns = [

    path('', include(router.urls))

]