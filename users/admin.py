"""Users Admin"""

# Django
from django.contrib import admin

# Models
from users.models import User


class CustomAdminUser(admin.ModelAdmin):
    """Custom admin user."""

    list_display = ['username', 'email', 'first_name', 'last_name', 'is_client', 'is_staff']
    list_filter = ['is_client', 'created', 'modified']


admin.site.register(User, CustomAdminUser)