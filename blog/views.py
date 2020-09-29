from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from .forms import PostForm
from django.utils import timezone


class PostListView(ListView):
    model = Post
    template_name = "blog/posts_list.html"
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"


class PostCreateView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request):
        return render(request, 'blog/post_create.html', context={'form': PostForm})

    def post(self, request):
        bound_form = PostForm(request.POST)

        if bound_form.is_valid():
            new_post = bound_form.save()
            new_post.author = request.user
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
            if new_post.draft_status == False:
                new_post.date_pub = timezone.now()
            new_post = bound_form.save()

            return redirect(new_post)
        else:
            return render(request, 'blog_update.html', context={'form': bound_form, 'post': post})
