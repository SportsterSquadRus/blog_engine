from django.shortcuts import render, redirect, reverse
from django.contrib.auth import models
from django.views import View
from django.views.generic import ListView
from author.models import Profile
from blog.models import Post
from .forms import ProfileForm
from allauth.socialaccount.models import SocialAccount


class UserPage(View):
    def get(self, request, pk):
        context = dict()
        user = models.User.objects.get(pk=pk)
        user_profile, created = Profile.objects.get_or_create(user=user)
        try:
            context['vk'] = SocialAccount.objects.get(user=user).get_profile_url()
        except:
            context['vk'] = ''
            
        context['rating'], context['part'], context['lvl_min'], context['lvl_max'], context['level'], context['posts'] = user_profile.rating(
            user)
        context['age'] = user_profile.age()
        context['author'] = user
        context['profile'] = user_profile
        return render(request, 'author/user_page.html', context=context)


class AuthorPostsView(ListView):
    model = Post
    paginate_by = 4
    context_object_name = 'posts'
    template_name = 'author/author_posts_list.html'

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
        user_profile, created = Profile.objects.get_or_create(user=user)
        profile_form = ProfileForm(instance=user_profile)
        return render(request, 'author/profile_edit.html', {'profile_form': profile_form})

    def post(self, request):
        user = models.User.objects.get(pk=request.user.id)
        user_profile, created = Profile.objects.get_or_create(user=user)
        profile_form = ProfileForm(request.POST, instance=user_profile)
        user_form = UserForm(request.POST, instance=user)

        if profile_form.is_valid():
            new_profile = profile_form.save()
            return redirect(reverse('user_page_url', args=[str(request.user.id)]))
        else:
            return render(request, 'author/profile_edit.html', {'profile_form': profile_form})
