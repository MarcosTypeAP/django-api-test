"""Project URLs"""

# Django
from django.contrib import admin
from django.urls import path, include


urlpatterns = [

    # Admin
    path('admin/', admin.site.urls),

    # Notes
    # path('', include(('notes.urls', 'notes'), namespace='notes')),

    # Users
    path('users/', include(('users.urls', 'users'), namespace='users')),

]
