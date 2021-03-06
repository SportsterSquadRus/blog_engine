from django.db import models
from django.contrib import auth
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from like.models import Like
from complaint.models import Complaint


class Comment(models.Model):
    author = models.ForeignKey(
        'auth.User', related_name='comment', on_delete=models.CASCADE, null=True)
    body = models.TextField(verbose_name='Текст комментярия')
    date_pub = models.DateTimeField(auto_now_add=True)
    likes = GenericRelation(Like)
    complaint = GenericRelation(Complaint)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    @property
    def total_likes(self):
        return self.likes.count()

    def likeOrNot(self, user):
        return True if len(self.likes.filter(user=user)) == 0 else False

    def complaintOrNot(self, user):
        return True if len(self.complaint.filter(user=user)) == 0 else False
