from django.urls import path
from .views import TagListView, TagDetailView


urlpatterns = [
    path('', TagListView.as_view(), name='tag_list_url'),
    path('detail/<int:id>/', TagDetailView.as_view(), name='tag_detail_url'),
]
