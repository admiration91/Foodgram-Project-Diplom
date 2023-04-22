from django.contrib import admin
from django.contrib.admin import register

from .models import User


@register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'first_name', 'last_name', 'email')
    search_fields = ('username', )
