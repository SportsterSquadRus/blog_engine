from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from .forms import PostForm
from comment.forms import CommentForm
from django.utils import timezone
from tag.models import Tag
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from .utils import banned_tags_check
from author.models import Profile


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


class PostDetailView(View):

    def get(self, request, pk):

        user_profile, created = Profile.objects.get_or_create(user=request.user)

        post = get_object_or_404(Post, pk=pk)
        context = dict()
        context['level'] = user_profile.rating(request.user)[4]
        context['post'] = post
        context['comment_form'] = CommentForm
        context['comments'] = post.comments.all()
        return render(request, "blog/post_detail.html", context=context)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        bound_form = CommentForm(request.POST)
        if bound_form.is_valid(): #and 'comment_pause' not in request.session:
            new_comment = bound_form.save()
            new_comment.author = request.user
            new_comment.content_type = ContentType.objects.get_for_model(Post)
            new_comment.object_id = post.id
            new_comment.save()
            # request.session.set_expiry(10)
            # request.session['comment_pause'] = True
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

        if bound_form.is_valid(): #and 'post_pause' not in request.session:

            new_post = bound_form.save()
            new_post.author = request.user
            if '<hr />' in new_post.body:
                new_post.truncate = len(
                    new_post.body[:new_post.body.find('<hr />')])
            else:
                new_post.truncate = 50

            if new_post.draft_status == False:
                new_post.date_pub = timezone.now()
            new_post.save()

            tags_list = set(request.POST['tags'].split(' '))
            clean_tags = banned_tags_check(tags_list)
            for tag in clean_tags:
                new_tag, created = Tag.objects.get_or_create(tag_title=tag)
                new_post.tags.add(new_tag)
            # request.session.set_expiry(60)
            # request.session['post_pause'] = True

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
        tags = ' '.join(map(lambda x:x.tag_title, post.tags.all()))

        return render(request, 'blog/post_update.html', context={'form': bound_form, 'post': post, 'post_tags': tags})

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        bound_form = PostForm(request.POST, instance=post)
        tags = ' '.join(map(lambda x:x.tag_title, post.tags.all()))

        if bound_form.is_valid():
            new_post = bound_form.save()
            if '<hr />' in new_post.body:
                new_post.truncate = len(
                    new_post.body[:new_post.body.find('<hr />')])
            else:
                new_post.truncate = 50
            if post.draft_status == True and new_post.draft_status == False:
                new_post.date_pub = timezone.now()
            new_post = bound_form.save()

            tags_list = set(request.POST['tags'].split(' '))
            clean_tags = banned_tags_check(tags_list)
            post.tags.clear()
            for tag in clean_tags:
                new_tag, created = Tag.objects.get_or_create(tag_title=tag)                
                new_post.tags.add(new_tag)

            return redirect(new_post)
        else:
            return render(request, 'blog_update.html', context={'form': bound_form, 'post': post, 'post_tags': tags})
