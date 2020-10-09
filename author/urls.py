from django.urls import path
from .views import UserPage, AuthorPostsView

urlpatterns = [
        path('<int:pk>/', UserPage.as_view(), name='user_page_url'),
        path('posts/<str:username>/', AuthorPostsView.as_view(), name='author_posts_list_url'),
]