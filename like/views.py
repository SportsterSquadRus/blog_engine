from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from .models import Like

@login_required
def ObjectLikeFunc(request, pk, model):
    obj = get_object_or_404(model, id=request.POST.get('obj_id'))
    obj_type = ContentType.objects.get_for_model(obj)
    if obj.likeOrNot(request.user):
        like, is_created = Like.objects.get_or_create(
            content_type=obj_type, object_id=obj.id, user=request.user)
    else:
        Like.objects.filter(content_type=obj_type,
                            object_id=obj.id, user=request.user).delete()
