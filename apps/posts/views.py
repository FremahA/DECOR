import logging
from unicodedata import category

import django_filters
from django.db.models import query
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import PostNotFound
from .models import Post, PostSaves, Category
from .serializers import (PostSerializer, PostCreateSerializer,
                          PostSavesSerializer, CategorySerializer)

logger = logging.getLogger(__name__)


class PostFilter(django_filters.FilterSet):
    category = django_filters.Filter(
    field_name="category", lookup_expr="in"
    )

    class Meta:
        model = Post
        fields = ["category"]


class ListAllPostsAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by("-created_at")
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = PostFilter
    search_fields = ["category", "title"]
    ordering_fields = ["created_at"]


class UserPostsAPIView(generics.ListAPIView):

    serializer_class = PostSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = PostFilter
    search_fields = ["category", "title"]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.filter(user=user).order_by("-created_at")
        return queryset


class PostSavesAPIView(generics.ListAPIView):
    serializer_class = PostSavesSerializer
    queryset = PostSaves.objects.all()


class PostDetailView(APIView):
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        user = request.user

        if not PostSaves.objects.filter(post=post, user=user).exists():
            PostSaves.objects.create(post=post, user=user)

            post.saves += 1
            post.save()

        serializer = PostSerializer(post, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


@api_view(["PUT"])
@permission_classes([permissions.IsAuthenticated])
def update_post_api_view(request, uuid):
    try:
        post = Post.objects.get(uuid=uuid)
    except Post.DoesNotExist:
        raise PostNotFound

    user = request.user
    if post.user != user:
        return Response(
            {"error": "You can't update or edit a post that doesn't belong to you"},
            status=status.HTTP_403_FORBIDDEN,
        )
    if request.method == "PUT":
        data = request.data
        serializer = PostSerializer(post, data, many=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



@permission_classes([permissions.IsAuthenticated])
@api_view(["POST"])
def create_post_api_view(request):
    user = request.user
    data = request.data
    data["user"] = request.user.id
    serializer = PostCreateSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        logger.info(
            f"New post {serializer.data.get('title')} created by {user.username}"
        )
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def delete_post_api_view(request, uuid):
    try:
        post = Post.objects.get(uuid=uuid)
    except Post.DoesNotExist:
        raise PostNotFound

    user = request.user
    if post.user != user:
        return Response(
            {"error": "You can't delete a post that doesn't belong to you"},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == "DELETE":
        delete_operation = post.delete()
        data = {}
        if delete_operation:
            data["success"] = "Deletion was successful"
        else:
            data["failure"] = "Deletion failed"
        return Response(data=data)


@api_view(["POST"])
def uploadPostImage(request):
    data = request.data

    post_uuid = data["post_uuid"]
    post = Post.objects.get(uuid=post_uuid)
    post.photo = request.FILES.get("photo")
    post.save()
    return Response("Image uploaded")


class PostSearchAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PostCreateSerializer

    def post(self, request):
        queryset = Post.objects.filter(is_published=True)
        data = self.request.data

        category = data["category"]
        queryset = queryset.filter(category__name__iexact=category)

        title = data["title"]
        queryset = queryset.filter(title__icontains=title)

        description = data["description"]
        queryset = queryset.filter(description__icontains=description)

        serializer = PostSerializer(queryset, many=True)

        return Response(serializer.data)