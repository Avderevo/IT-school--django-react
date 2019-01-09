from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile, Activation


@admin.register(Profile, Activation)
class UserAdmin(admin.ModelAdmin):
    pass