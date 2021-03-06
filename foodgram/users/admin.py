from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_filter = ("email", "username")
