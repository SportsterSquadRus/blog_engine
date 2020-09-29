from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostDeleteView, PostUpdateView

urlpatterns = [
    path('', PostListView.as_view(), name='posts_list_url'),
    path('post/detail/<int:pk>/', PostDetailView.as_view(), name='post_detail_url'),
    path('post/create/', PostCreateView.as_view(), name='post_create_url'),
    path('post/detail/<int:pk>/', PostDetailView.as_view(), name='post_detail_url'),
    path('post/delete/<int:pk>', PostDeleteView.as_view(), name='post_delete_url'),
    path('post/update/<int:pk>', PostUpdateView.as_view(), name='post_update_url'),
]