from django.urls import path
from .views import SearchView, PostsListView, PostDetailView, PostCreateView, PostDeleteView, PostUpdateView, AuthorPostsView, DraftsListView, TagListView, TagDetailView, PostLikeView

urlpatterns = [
    path('', PostsListView.as_view(), name='posts_list_url'),
    path('post/detail/<int:pk>/', PostDetailView.as_view(), name='post_detail_url'),
    path('post/create/', PostCreateView.as_view(), name='post_create_url'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete_url'),
    path('post/update/<int:pk>/', PostUpdateView.as_view(), name='post_update_url'),
    path('author/<str:username>/', AuthorPostsView.as_view(), name='author_posts_list_url'),
    path('drafts/', DraftsListView.as_view(), name='drafts_list_url'),
    path('tags/', TagListView.as_view(), name='tag_list_url'),
    path('tag/detail/<str:slug>/', TagDetailView.as_view(), name='tag_detail_url'),
    path('like/<int:pk>/', PostLikeView, name='like_post'),
    path('search/', SearchView.as_view(), name='search_posts_url')
]
