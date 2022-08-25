from django.contrib import admin
from .models import Post, PostSaves

class PostAdmin(admin.ModelAdmin):
    list_display = ["title",  "user"]
    

admin.site.register(Post, PostAdmin)
admin.site.register(PostSaves)
