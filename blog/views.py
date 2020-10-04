from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from .forms import PostForm
from django.utils import timezone
from django.contrib.auth import models
from taggit.models import Tag
from django.db.models import Q


class PostsListView(ListView):
    model = Post
    queryset = Post.objects.filter(draft_status=False)
    template_name = "blog/posts_list.html"
    context_object_name = 'posts'
    paginate_by = 4


class AuthorPostsView(View):
    def get(self, request, username):
        user = models.User.objects.get(username=username)
        return render(request, 'blog/author_posts_list.html', context={'posts': Post.objects.filter(author=user, draft_status=False)})


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"


class SearchView(ListView):
    paginate_by = 4
    template_name = "blog/posts_list.html"
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(Q(title__icontains=self.request.GET.get('q')) | Q(body__icontains=self.request.GET.get('q')))

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context
    


class PostCreateView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request):
        return render(request, 'blog/post_create.html', context={'form': PostForm})

    def post(self, request):
        bound_form = PostForm(request.POST)

        if bound_form.is_valid():
            new_post = bound_form.save()
            new_post.author = request.user
            if '<cut>' in new_post.body:
                new_post.truncate = len(new_post.body[:new_post.body.find('<cut>')].split())
            else:
                new_post.truncate = 50
            if new_post.draft_status == False:
                new_post.date_pub = timezone.now()
            new_post.save()

            return redirect(new_post)
        else:
            return render(request, 'blog/post_create.html', context={'form': bound_form})


class PostDeleteView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk, author=request.user)
        return render(request, 'blog/post_delete.html', context={'post': post})

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect(reverse('posts_list_url'))


class PostUpdateView(LoginRequiredMixin, View):

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk, author=request.user)
        bound_form = PostForm(instance=post)
        return render(request, 'blog/post_update.html', context={'form': bound_form, 'post': post})

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        bound_form = PostForm(request.POST, instance=post)

        if bound_form.is_valid():
            new_post = bound_form.save()
            if '<cut>' in new_post.body:
                new_post.truncate = len(new_post.body[:new_post.body.find('<cut>')].split())
            else:
                new_post.truncate = 50
            if post.draft_status == True and new_post.draft_status == False:
                new_post.date_pub = timezone.now()
            new_post = bound_form.save()

            return redirect(new_post)
        else:
            return render(request, 'blog_update.html', context={'form': bound_form, 'post': post})


class DraftsListView(View):
    def get(self, request):
        posts = Post.objects.filter(author=request.user, draft_status=True)
        return render(request, 'blog/posts_list.html', {'posts': posts})



class TagListView(ListView):
    model = Tag
    template_name = "blog/tags_list.html"
    context_object_name = 'tags'
    ordering = ['name']
    paginate_by = 4

class TagDetailView(View):
    def get(self, request, slug):
        tag = get_object_or_404(Tag, slug__iexact=slug)
        return render(request, 'blog/tag_detail.html', context={'tag': tag, 'posts': Post.objects.filter(tags=tag, draft_status=False).order_by('-date_pub')})


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if request.user not in post.likes.all():
        post.likes.add(request.user)
    return redirect(reverse('post_detail_url', args=[str(pk)]))
