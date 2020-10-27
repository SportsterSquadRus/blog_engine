from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import models
from django.core.mail import send_mail
from blog_engine import passwords

def ObjectComplaintFunc(request, pk, model):
    obj = get_object_or_404(model, id=pk)
    user = models.User.objects.get(pk=request.user.id)
    send_mail(
    'Жалоба',
    'http://127.0.0.1:8000{}'.format(obj.get_absolute_url()),
    passwords.email_pass()[0],
    [passwords.stuff()],
    fail_silently=False,
)
