from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile, Activation
from django.contrib.auth.models import Group


admin.site.unregister(Group)

@admin.register(Profile, Activation)
class UserAdmin(admin.ModelAdmin):
    pass