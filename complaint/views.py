from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from blog.models import Post
from author.models import Profile
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import models
from django.core.mail import send_mail
from blog_engine import passwords

@login_required
def PostComplaintView(request, pk):
    obj = get_object_or_404(Post, id=pk)
    obj_type = ContentType.objects.get_for_model(obj)
    user = models.User.objects.get(pk=request.user.id)

    user = models.User.objects.get(pk=request.user.id)
    user_profile, created = Profile.objects.get_or_create(user=user)
    lvl = user_profile.rating(user)[4]

    send_mail('Жалоба на пост от пользователя {}.'.format(user), 'http://127.0.0.1:8000{}'.format(obj.get_absolute_url()), passwords.email_pass()[0], [passwords.stuff()], fail_silently=False,)
    return redirect(reverse('post_detail_url', args=[str(pk)]))

@login_required
def CommentComplaintView(request, pk):
    pass
