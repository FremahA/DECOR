from django.urls import path

from . import views

urlpatterns = [
    path("", views.ListAllPostsAPIView.as_view(), name="all-posts"),
    path("userposts/", views.UserPostsAPIView.as_view(), name="user-posts"),
    path("newpost/", views.create_post_api_view, name="post-create"),
    path("details/<slug:slug>/",views.PostDetailView.as_view(),name="post-details"),
    path("<uuid:uuid>/", views.update_post_api_view, name="update-post"),
    path("<slug:slug>/", views.delete_post_api_view, name="delete-post"),
    path("search/", views.PostSearchAPIView.as_view(), name="post-search"),
    path("categories/", views.CategoryView.as_view(), name="all-categories"),
]