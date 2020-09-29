from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostDeleteView, PostUpdateView, AuthorPostsView, DraftsListView

urlpatterns = [
    path('', PostListView.as_view(), name='posts_list_url'),
    path('post/detail/<int:pk>/', PostDetailView.as_view(), name='post_detail_url'),
    path('post/create/', PostCreateView.as_view(), name='post_create_url'),
    path('post/detail/<int:pk>/', PostDetailView.as_view(), name='post_detail_url'),
    path('post/delete/<int:pk>', PostDeleteView.as_view(), name='post_delete_url'),
    path('post/update/<int:pk>', PostUpdateView.as_view(), name='post_update_url'),
    path('author/<str:username>/', AuthorPostsView.as_view(), name='author_posts_list_url'),
    path('drafts/', DraftsListView.as_view(), name='drafts_list_url')
]