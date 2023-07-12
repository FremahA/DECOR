from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["uuid", "id", "user", "gender", "country"]
    list_filter = ["gender", "country"]
    list_display_links = ["uuid", "id", "user"]

admin.site.register(Profile, ProfileAdmin)