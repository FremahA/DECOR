from rest_framework import serializers
from .models import Post, Category, PostSaves

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.JSONField()
    class Meta:
        model = Category
        fields = ["name"] 


class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    photo = serializers.SerializerMethodField()
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ["category", "user", "photo", "title", "slug", "description", "website", "is_published", "saves", "uuid", "saves"] 


    def get_user(self, obj):
        return obj.user.username

    def get_category(self, obj):
        return obj.category.category.name

    def get_photo(self, obj):
        return obj.photo.url


class PostCreateSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)

    class Meta:
        model = Post
        fields = ["category", "user", "photo", "title", "slug", "description", "website", "is_published", "saves", "uuid", "saves"] 


class PostSavesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostSaves 
        exclude = ["updated_at", "id"] 
