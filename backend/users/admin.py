from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'first_name', 'last_name', 'email')
    search_fields = ('username', 'first_name', 'last_name')
    list_filter = ('email',)
    empty_value_display = '---'


admin.site.register(User, UserAdmin)
