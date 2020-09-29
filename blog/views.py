from django.shortcuts import render
from django.views.generic import View, ListView, DetailView
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = "blog/posts_list.html"

