
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from .models import Like
from comment.models import Comment
from blog.models import Post
from author.models import Profile
from django.contrib.auth import models


@login_required
def ObjectLikeFunc(request, pk, model):
    obj = get_object_or_404(model, id=request.POST.get('obj_id'))
    obj_type = ContentType.objects.get_for_model(obj)

    user = models.User.objects.get(pk=request.user.id)
    user_profile, created = Profile.objects.get_or_create(user=user)
    lvl = user_profile.rating(user)[4]

    if obj.likeOrNot(request.user):
        if lvl > 1:
            like, is_created = Like.objects.get_or_create(
                content_type=obj_type, object_id=obj.id, user=request.user)

    else:
        Like.objects.filter(content_type=obj_type,
                            object_id=obj.id, user=request.user).delete()


def PostLikeView(request, pk):
    ObjectLikeFunc(request, pk, Post)
    return redirect(reverse('post_detail_url', args=[str(pk)]))


def CommentLikeView(request, pk):
    ObjectLikeFunc(request, pk, Comment)
    comment = Comment.objects.get(pk=pk)

    return redirect(reverse('post_detail_url', args=[str(comment.object_id)]))
