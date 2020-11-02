
from django.shortcuts import redirect, reverse
from django.contrib.auth.decorators import login_required
from comment.models import Comment
from blog.models import Post
from .utils import ObjectLikeFunc
from django.http import HttpResponse
import json


@login_required
def PostLikeView(request, pk):
    if request.method == 'POST':
        if request.POST.get("operation") == "like_submit" and request.is_ajax():
            liked, total_likes = ObjectLikeFunc(request, pk, Post)
            ctx = {'liked': liked, "content_id":pk, 'likes_count':total_likes}
            return HttpResponse(json.dumps(ctx), content_type='application/json')

    ObjectLikeFunc(request, pk, Post)
    return redirect(reverse('post_detail_url', args=[str(pk)]))

@login_required
def CommentLikeView(request, pk):
    if request.method == 'POST':
        if request.POST.get("operation") == "like_submit" and request.is_ajax():
            liked, total_likes = ObjectLikeFunc(request, pk, Comment)
            ctx = {'liked': liked, "content_id":pk, 'likes_count':total_likes}
            return HttpResponse(json.dumps(ctx), content_type='application/json')

    ObjectLikeFunc(request, pk, Comment)
    comment = Comment.objects.get(pk=pk)

    return redirect(reverse('post_detail_url', args=[str(comment.object_id)]))
