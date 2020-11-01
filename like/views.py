
from django.shortcuts import redirect, reverse
from django.contrib.auth.decorators import login_required
from comment.models import Comment
from blog.models import Post
from .utils import ObjectLikeFunc


@login_required
def PostLikeView(request, pk):
    ObjectLikeFunc(request, pk, Post)
    return redirect(reverse('post_detail_url', args=[str(pk)]))

@login_required
def CommentLikeView(request, pk):
    ObjectLikeFunc(request, pk, Comment)
    comment = Comment.objects.get(pk=pk)

    return redirect(reverse('post_detail_url', args=[str(comment.object_id)]))
