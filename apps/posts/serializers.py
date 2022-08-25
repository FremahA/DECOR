from rest_framework import serializers
from .models import Post, Category, PostSaves

class CategorySerializer(serializers.Serializer):
    name = serializers.SerializerMethodField

    class Meta:
        model = Category


class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    photo = serializers.SerializerMethodField()
    category = CategorySerializer(many=True)

    class Meta:
        model = Post
        exclude = ["updated_at", "id"]

    def get_user(self, obj):
        return obj.user.username

    def get_category(self, obj):
        return obj.category.name 

    def get_photo(self, obj):
        return obj.photo.url  

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ["updated_at", "pkid"]

class PostSavesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostSaves 
        exclude = ["updated_at", "pkid"]       