from django.contrib import admin
from .models import Post, PostSaves, Category

class PostAdmin(admin.ModelAdmin):
    list_display = ["title",  "user", 'slug']
    readonly_fields = ('slug', 'uuid', "saves")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]

admin.site.register(Post, PostAdmin)
admin.site.register(PostSaves)
admin.site.register(Category, CategoryAdmin)
