
from django.urls import path
from .views import SearchView, PostsListView, PostDetailView, PostCreateView, PostDeleteView, PostUpdateView, DraftsListView, TagListView, TagDetailView

urlpatterns = [
    path('', PostsListView.as_view(), name='posts_list_url'),

    path('post/detail/<int:pk>/', PostDetailView.as_view(), name='post_detail_url'),
    path('post/create/', PostCreateView.as_view(), name='post_create_url'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete_url'),
    path('post/update/<int:pk>/', PostUpdateView.as_view(), name='post_update_url'),
    path('drafts/', DraftsListView.as_view(), name='drafts_list_url'),
    path('tags/', TagListView.as_view(), name='tag_list_url'),
    path('tag/detail/<str:slug>/', TagDetailView.as_view(), name='tag_detail_url'),
    path('search/', SearchView.as_view(), name='search_posts_url'),    
]