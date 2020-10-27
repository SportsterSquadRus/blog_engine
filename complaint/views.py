from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from blog.models import Post
from django.core.mail import send_mail
from blog_engine import passwords
from .utils import ObjectComplaintFunc


@login_required
def PostComplaintView(request, pk):
    post = ObjectComplaintFunc(request, pk, Post)

    send_mail('Жалоба на пост от пользователя {}.'.format(request.user), 'http://127.0.0.1:8000{}'.format(
        post.get_absolute_url()), passwords.email_pass()[0], [passwords.stuff()], fail_silently=False,)
    return redirect(reverse('post_detail_url', args=[str(pk)]))


@login_required
def CommentComplaintView(request, pk):
    pass
