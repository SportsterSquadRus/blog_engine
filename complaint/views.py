from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from blog.models import Post
from comment.models import Comment
from django.core.mail import send_mail
from blog_engine import passwords
from .utils import ObjectComplaintFunc


@login_required
def PostComplaintView(request, pk):
    post, comp = ObjectComplaintFunc(request, pk, Post)
    if comp:
        send_mail('Жалоба на пост от пользователя {}.'.format(request.user), 'http://127.0.0.1:8000{}'.format(
            post.get_absolute_url()), passwords.email_pass()[0], [passwords.stuff()], fail_silently=False,)
    return redirect(reverse('post_detail_url', args=[str(pk)]))


@login_required
def CommentComplaintView(request, pk):
    comment, comp = ObjectComplaintFunc(request, pk, Comment)
    print(comment)
    if comp:
        post = Post.objects.get(id=comment.object_id)

        send_mail('Жалоба на комментарий от пользователя {}.'.format(request.user), 'Комментарий к посту http://127.0.0.1:8000{}. Текст комментария: {}'.format(
            post.get_absolute_url(), comment.body), passwords.email_pass()[0], [passwords.stuff()], fail_silently=False,)
    return redirect(reverse('post_detail_url', args=[str(comment.object_id)]))


