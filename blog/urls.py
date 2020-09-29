from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView

urlpatterns = [
    path('', PostListView.as_view(), name='posts_list_url'),
    path('post/detail/<int:pk>/', PostDetailView.as_view(), name='post_detail_url'),
    path('post/create/', PostCreateView.as_view(), name='post_create_url'),
    path('post/detail/<int:pk>/', PostDetailView.as_view(), name='post_detail_url'),
]