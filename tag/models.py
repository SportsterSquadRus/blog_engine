from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Tag(models.Model):
    tag_title = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.tag_title
