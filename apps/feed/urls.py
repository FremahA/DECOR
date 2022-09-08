from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserCategoryViewset, UserFeedAPIView

app_name = "feed"

router = DefaultRouter()
router.register('', UserCategoryViewset, basename='user-categories')

urlpatterns = [
    path('user-feed/', UserFeedAPIView.as_view(), name="user-feed"),
    path("", include(router.urls))
]
