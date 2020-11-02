from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from blog.models import Post
from comment.models import Comment
from django.core.mail import send_mail
from blog_engine import passwords
from .utils import ObjectComplaintFunc
from django.http import HttpResponse
import json


@login_required
def PostComplaintView(request, pk):
    if request.method == 'POST':
        if request.POST.get("operation") == "complaint_submit" and request.is_ajax():
            print('ohoh')
            post, comp = ObjectComplaintFunc(request, pk, Post)
            if comp:
                send_mail('Жалоба на пост от пользователя {}.'.format(request.user), 'http://127.0.0.1:8000{}'.format(
                    post.get_absolute_url()), passwords.email_pass()[0], [passwords.admin()], fail_silently=False,)
                
                ctx = {'complaint': comp, "content_id":pk}

                return HttpResponse(json.dumps(ctx), content_type='application/json')

    post, comp = ObjectComplaintFunc(request, pk, Post)
    if comp:
        send_mail('Жалоба на пост от пользователя {}.'.format(request.user), 'http://127.0.0.1:8000{}'.format(
            post.get_absolute_url()), passwords.email_pass()[0], [passwords.admin()], fail_silently=False,)
    return redirect(reverse('post_detail_url', args=[str(pk)]))


@login_required
def CommentComplaintView(request, pk):
    comment, comp = ObjectComplaintFunc(request, pk, Comment)
    if comp:
        post = Post.objects.get(id=comment.object_id)

        send_mail('Жалоба на комментарий от пользователя {}.'.format(request.user), 'Комментарий к посту http://127.0.0.1:8000{}. Текст комментария: {}'.format(
            post.get_absolute_url(), comment.body), passwords.email_pass()[0], [passwords.admin()], fail_silently=False,)
    return redirect(reverse('post_detail_url', args=[str(comment.object_id)]))
