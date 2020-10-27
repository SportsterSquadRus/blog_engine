from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import models
from author.models import Profile
from .models import Complaint



def ObjectComplaintFunc(request, pk, model):
    obj = get_object_or_404(model, id=pk)
    obj_type = ContentType.objects.get_for_model(obj)

    user = models.User.objects.get(pk=request.user.id)
    user_profile, created = Profile.objects.get_or_create(user=user)
    lvl = user_profile.rating(user)[4]
    if obj.complaintOrNot(request.user):
        if lvl > 1:
            complaint, is_created = Complaint.objects.get_or_create(
                content_type=obj_type, object_id=obj.id, user=request.user)
            return obj
