from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from comment.models import Comment
from like.models import Like
from .forms import PostForm
from comment.forms import CommentForm
from django.utils import timezone
from django.contrib.auth import models
from taggit.models import Tag
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from like.views import ObjectLikeFunc
from author.models import Profile



def PostLikeView(request, pk):
    ObjectLikeFunc(request, pk, Post)
    return redirect(reverse('post_detail_url', args=[str(pk)]))

def CommentLikeView(request, pk):
    ObjectLikeFunc(request, pk, Comment)
    comment = Comment.objects.get(pk=pk)

    return redirect(reverse('post_detail_url', args=[str(comment.object_id)]))

class UserPage(View):
    def get(self, request, pk):
        user = models.User.objects.get(pk=pk)
        user_profile, created = Profile.objects.get_or_create(user=user)
        rating, part, lvl_min, lvl_max, level, posts = user_profile.rating(user) 
        return render(request, 'blog/user_page.html', context={'author': user, 'posts': posts, 'rating': rating, 'level': level, 'lvl_max': lvl_max, 'lvl_min': lvl_min, 'part': part})



class PostsListView(ListView):
    model = Post
    queryset = Post.objects.filter(draft_status=False)
    template_name = "blog/posts_list.html"
    context_object_name = 'posts'
    paginate_by = 4


class DraftsListView(ListView):
    model = Post
    template_name = "blog/drafts_list.html"
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user, draft_status=True)


class AuthorPostsView(ListView):
    model = Post
    paginate_by = 4
    context_object_name = 'posts'
    template_name = 'blog/author_posts_list.html'

    def get_queryset(self):
        user = models.User.objects.get(username=self.kwargs['username'])
        return Post.objects.filter(author=user, draft_status=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = models.User.objects.get(username=self.kwargs['username'])
        return context


class PostDetailView(View):

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        context = dict()
        context['post'] = post
        context['comment_form'] = CommentForm
        context['comments'] = post.comments.all()
        return render(request, "blog/post_detail.html", context=context)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        bound_form = CommentForm(request.POST)
        if bound_form.is_valid():
            new_comment = bound_form.save()
            new_comment.author = request.user
            new_comment.content_type = ContentType.objects.get_for_model(Post)
            new_comment.object_id = post.id
            new_comment.save()
            return redirect(reverse('post_detail_url', args=[str(pk)]))
        else:
            context = {'post': post, 'comment_form': CommentForm,
                       'comments': post.comments.all()}
            return render(request, "blog/post_detail.html", context=context)


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
            if '----------' in new_post.body:
                new_post.truncate = len(
                    new_post.body[:new_post.body.find('----------')])
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
            if '----------' in new_post.body:
                new_post.truncate = len(
                    new_post.body[:new_post.body.find('----------')])
            else:
                new_post.truncate = 50
            if post.draft_status == True and new_post.draft_status == False:
                new_post.date_pub = timezone.now()
            new_post = bound_form.save()

            return redirect(new_post)
        else:
            return render(request, 'blog_update.html', context={'form': bound_form, 'post': post})


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
        tag = get_object_or_404(Tag, slug__iexact=self.kwargs['slug'])
        return Post.objects.filter(tags=tag, draft_status=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug__iexact=self.kwargs['slug'])
        return context
