from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from .models import Like
from author.models import Profile
from django.contrib.auth import models

def ObjectLikeFunc(request, pk, model):

    obj = get_object_or_404(model, id=request.POST.get('content_id'))
    obj_type = ContentType.objects.get_for_model(obj)



    user = models.User.objects.get(pk=request.user.id)
    user_profile, created = Profile.objects.get_or_create(user=user)
    lvl = user_profile.rating(user)[4]
    liked = obj.likeOrNot(request.user)
    if liked:
        if lvl > 1:
            like, is_created = Like.objects.get_or_create(
                content_type=obj_type, object_id=obj.id, user=request.user)

    else:
        Like.objects.filter(content_type=obj_type,
                            object_id=obj.id, user=request.user).delete()
    return liked, obj.total_likes