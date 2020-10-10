from django.shortcuts import render
from django.contrib.auth import models
from django.views import View
from django.views.generic import ListView
from author.models import Profile
from blog.models import Post
from .forms import ProfileForm, UserForm


class UserPage(View):
    def get(self, request, pk):
        user = models.User.objects.get(pk=pk)
        user_profile, created = Profile.objects.get_or_create(user=user)
        rating, part, lvl_min, lvl_max, level, posts = user_profile.rating(
            user)
        return render(request, 'blog/user_page.html', context={'author': user, 'posts': posts, 'rating': rating, 'level': level, 'lvl_max': lvl_max, 'lvl_min': lvl_min, 'part': part})


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
        context['author'] = models.User.objects.get(
            username=self.kwargs['username'])
        return context


class ProfileEditView(View):
    def get(self, request):
        user = models.User.objects.get(pk=request.user.id)
        print(user)
        print(user.username)
        print(user.email)

        user_profile, created = Profile.objects.get_or_create(user=user)
        profile_form = ProfileForm(instance=user_profile)
        user_form = UserForm(instance=user)
        return render(request, 'blog/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})
