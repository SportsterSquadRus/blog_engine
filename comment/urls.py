from django.urls import path
from .views import AddCommentView

urlpatterns = [
    path('<int:pk>/', AddCommentView.as_view(), name='add_comment_url')
]