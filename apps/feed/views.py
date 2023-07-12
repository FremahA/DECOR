import logging

from django.db.models import query

from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import  UserCategoryCreateSerializer, UserCategorySerializer
from .models import UserCategory

from apps.posts.models import Post
from apps.posts.serializers import PostSerializer

logger = logging.getLogger(__name__)


class UserCategoryViewset(viewsets.ModelViewSet):
    queryset = UserCategory.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request):
        data = request.data
        data["user"] = request.user.id
        serializer_class = UserCategoryCreateSerializer(data=data)
        if serializer_class.is_valid():
            serializer_class.save
        return Response(serializer_class.data)
        
    def update(self, request, pk=None):
        instance = UserCategory.objects.get(user=request.user)
        serializer_class = UserCategoryCreateSerializer(instance, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save
        return Response(serializer_class.data)

    def list(self, request):
        queryset = UserCategory.objects.all()
        serializer_class = UserCategorySerializer(queryset, many=True)
        return Response(serializer_class.data)


class UserFeedAPIView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get(self, request):
        user = request.user
        category = UserCategory.objects.get(user=user).category_following.all()
        queryset = Post.objects.filter(category__in=category)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)




