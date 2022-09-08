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


# @permission_classes([permissions.IsAuthenticated])
# @api_view(["POST"])
# def create_usercategory_api_view(request):
#     user = request.user
#     data = request.data
#     data["user"] = request.user.id
#     serializer = UserCategoryCreateSerializer(data=data)

#     if serializer.is_valid():
#         serializer.save()
#         logger.info(
#             f"New categories, {serializer.data.get('category_following')} followed by {user.username}"
#         )
#         return Response(serializer.data)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


# @permission_classes([permissions.IsAuthenticated])
# @api_view(["PUT"])
# def update_usercategory_api_view(request):
#     user = request.user
#     # try:
#     instance = UserCategory.objects.get(user=user)
#     # except UserCategory.DoesNotExist:
#     #     raise UserCategoryNotFound  

#     # user = request.user
#     # if instance.user != user:
#     #     return Response(
#     #         {"error": "You can't update or edit another user's categories"},
#     #         status=status.HTTP_403_FORBIDDEN,
#     #     )  

#     # if request.method == "PUT":

#     data = request.data
#     serializer = UserCategoryCreateSerializer(instance, data=data, many=False)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data)

#     # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 






