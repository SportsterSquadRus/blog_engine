from django.urls import path
from .views import PostComplaintView, CommentComplaintView

urlpatterns = [
    path('post/<int:pk>/', PostComplaintView, name='complaint_post'),
    path('comment/<int:pk>/', CommentComplaintView, name='complaint_comment'),
]