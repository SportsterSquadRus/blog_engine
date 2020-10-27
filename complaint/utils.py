from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import models

def ObjectComplaintFunc(request, pk, model):
    obj = get_object_or_404(model, id=pk)
    user = models.User.objects.get(pk=request.user.id)
