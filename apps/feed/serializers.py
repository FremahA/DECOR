from rest_framework import serializers
from .models import UserCategory
from apps.posts.serializers import CategorySerializer


class UserCategorySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    category_following = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = UserCategory
        fields = ["user", "category_following", "uuid", "id"]
    def get_user(self, obj):
        return obj.user.username

    def get_category_following(self, obj):
            return obj.category_following.category.name


class UserCategoryCreateSerializer(serializers.ModelSerializer):
    category_following = CategorySerializer(many=True)

    class Meta:
        model = UserCategory
        fields = ["user", "category_following", "uuid", "id"]


    def update(self, instance, validated_data):
        category_following = validated_data.pop('category_following')
        instance.category_following.set(category_following)
        return instance

