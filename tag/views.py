from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Tag
from blog.models import Post


class TagListView(ListView):
    model = Tag
    template_name = "blog/tags_list.html"
    context_object_name = 'tags'
    ordering = ['name']
    paginate_by = 4


class TagDetailView(ListView):
    model = Post
    template_name = "blog/tag_detail.html"
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self, **kwargs):
        tag = get_object_or_404(Tag, id=self.kwargs['id'])
        return Post.objects.filter(tags=tag, draft_status=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(id=self.kwargs['id'])
        return context
