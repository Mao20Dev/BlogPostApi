from django.urls import path
from . import views


urlpatterns = [
    path('blogposts/', views.BlogPostListCreate.as_view(), name="blog_post_view_create"),
    path('blogposts/<int:pk>', views.BlogPostRetrieveUpdateDestroy.as_view(), name="update"),
    path('blogposts/search/', views.BlogPostList.as_view(), name="filter"),
]
