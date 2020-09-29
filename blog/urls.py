from django.urls import path
from .views import PostListView, PostCreateView

urlpatterns = [
    path('', PostListView.as_view(), name='posts_list_url'),
    path('post/create/', PostCreateView.as_view(), name='post_create_url')
]