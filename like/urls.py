from .views import PostLikeView, CommentLikeView
from django.urls import path

urlpatterns = [
    path('post/<int:pk>/', PostLikeView, name='like_post'),
    path('comment/<int:pk>/', CommentLikeView, name='like_comment'),
    
]