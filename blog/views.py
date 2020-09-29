from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from .forms import PostForm


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
            new_post.save()
            return redirect('posts_list_url')
        else:
            return render(request, 'blog/post_create.html', context={'form': bound_form})
