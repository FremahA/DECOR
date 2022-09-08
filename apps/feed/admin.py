from django.contrib import admin
from .models import UserCategory


class UserCategoryAdmin(admin.ModelAdmin):
    list_display = [ "user", "uuid"]
    readonly_field = ('uuid')

admin.site.register(UserCategory, UserCategoryAdmin)
