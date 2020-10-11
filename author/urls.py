from django.urls import path
from .views import UserPage, AuthorPostsView, ProfileEditView

urlpatterns = [
    path('<int:pk>/', UserPage.as_view(), name='user_page_url'),
    path('posts/<str:username>/', AuthorPostsView.as_view(),
         name='author_posts_list_url'),
    path('edit/', ProfileEditView.as_view(), name='profile_edit_url')
]
